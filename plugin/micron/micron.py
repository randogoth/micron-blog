import os
import re

from pelican import signals
from pelican.writers import Writer
from pelican.paginator import Paginator
from pelican.readers import MarkdownReader, DUPLICATES_DEFINITIONS_ALLOWED
from pelican.utils import get_relative_path, is_selected_for_writing, path_to_url, sanitised_join, pelican_open

from markdown.extensions.meta import BEGIN_RE, META_RE, META_MORE_RE, END_RE

from mistune import Markdown
from mistune.core import BlockState
from mistune.util import strip_end
from mistune.renderers._list import render_list
from mistune.renderers.markdown import MarkdownRenderer

from typing import Dict, Any
from textwrap import indent

# === U N D E R L I N E D   M I S T U N E   P L U G I N ===
# from https://github.com/randogoth/md2mu

UNDERLINED = r'\b_{1,3}(?=[^\s_])'
UNDERLINED_END_RE = {
    '_': re.compile(r'(?:(?<!\\)(?:\\\\)*\\_|[^\s_])_(?!_)\b'),
    '__': re.compile(r'(?:(?<!\\)(?:\\\\)*\\_|[^\s_])__(?!_)\b'),
    '___': re.compile(r'(?:(?<!\\)(?:\\\\)*\\_|[^\s_])___(?!_)\b'),
}

def parse_underlined(self, m, state) -> int:
        pos = m.end()
        marker = m.group(0)
        mlen = len(marker)
        _end_re = UNDERLINED_END_RE[marker]
        m1 = _end_re.search(state.src, pos)
        if not m1:
            state.append_token({'type': 'text', 'raw': marker})
            return pos
        end_pos = m1.end()
        text = state.src[pos:end_pos-mlen]
        prec_pos = self.precedence_scan(m, state, end_pos)
        if prec_pos:
            return prec_pos
        new_state = state.copy()
        new_state.src = text
        new_state.in_underlined = True
        state.append_token({
            'type': 'underlined',
            'children': self.render(new_state),
        })
        return end_pos

def render_underlined_mu(self, token, state) -> str:
        return '`_' + self.render_children(token, state) + '`_'

def render_underlined_html(self, token, state) -> str:
        return '<u>' + self.render_children(token, state) + '</u>'

# === M I C R O N   R E N D E R E R   F O R   M I S T U N E ===
# from https://github.com/randogoth/md2mu

class MicronRenderer(MarkdownRenderer):
    """A renderer to format Micron text."""
    NAME = 'micron'

    def __call__(self, tokens, state: BlockState):
        out = self.render_tokens(tokens, state)
        # special handle for line breaks
        out += '\n\n'.join(self.render_referrences(state)) + '\n'
        return strip_end(out)
    
    def render_children(self, token, state: BlockState):
        children = token['children']
        return self.render_tokens(children, state)

    def text(self, token: Dict[str, Any], state: BlockState) -> str:
        return token['raw']
    
    def emphasis(self, token: Dict[str, Any], state: BlockState) -> str:
        return '`*' + self.render_children(token, state) + '`*'

    def strong(self, token: Dict[str, Any], state: BlockState) -> str:
        return '`!' + self.render_children(token, state) + '`!'
    
    def link(self, token: Dict[str, Any], state: BlockState) -> str:
        label = token.get('label')
        text = self.render_children(token, state)
        out = '`[' + text + '`'
        if label:
            return out + '`[' + label + '`'
        attrs = token['attrs']
        url = attrs['url']
        if text == url:
            return '`[' + text + '`'
        elif 'mailto:' + text == url:
            return '`[' + text + '`'
        out += url
        return out + ']'
    
    def image(self, token: Dict[str, Any], state: BlockState) -> str:
        return self.link(token, state)

    def codespan(self, token: Dict[str, Any], state: BlockState) -> str:
        return '`=' + token['raw'] + '`='

    def linebreak(self, token: Dict[str, Any], state: BlockState) -> str:
        return '  \n'
    
    def softbreak(self, token: Dict[str, Any], state: BlockState) -> str:
        return '\n'
    
    def blank_line(self, token: Dict[str, Any], state: BlockState) -> str:
        return ''
    
    def inline_html(self, token: Dict[str, Any], state: BlockState) -> str:
        return ''
    
    def paragraph(self, token: Dict[str, Any], state: BlockState) -> str:
        text = self.render_children(token, state)
        return text + '\n\n'

    def heading(self, token: Dict[str, Any], state: BlockState) -> str:
        level = token['attrs']['level']
        if level > 3:
            level = 3
        marker = '>' * level
        text = self.render_children(token, state)
        return marker + ' ' + text + '\n\n'
    def thematic_break(self, token: Dict[str, Any], state: BlockState) -> str:
        return '-\n\n'
    
    def block_text(self, token: Dict[str, Any], state: BlockState) -> str:
        return self.render_children(token, state) + '\n'
    
    def block_code(self, token: Dict[str, Any], state: BlockState) -> str:
        code = token['raw']
        if code and code[-1] != '\n':
            code += '\n'
        marker = '`='
        return marker + '\n' + code + marker + '\n\n'
    
    def block_quote(self, token: Dict[str, Any], state: BlockState) -> str:
        text = indent(self.render_children(token, state), '>>>>')
        return text + '\n\n'
    
    def block_html(self, token: Dict[str, Any], state: BlockState) -> str:
        return ''
    
    def block_error(self, token: Dict[str, Any], state: BlockState) -> str:
        return ''
    
    def list(self, token: Dict[str, Any], state: BlockState) -> str:
        return render_list(self, token, state)

# === M A R K D O W N   T O   M I C R O N   R E A D E R ===

class MarkdownToMicronReader(MarkdownReader):
    enabled = True
    file_extensions = ['md', 'markdown', 'mkd', 'mdown']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _parse_metadata(self, meta):
        """Return the dict containing document metadata"""
        output = {}
        for name, value in meta.items():
            name = name.lower()
            if not DUPLICATES_DEFINITIONS_ALLOWED.get(name, True):
                output[name] = self.process_metadata(name, value[0])
            elif len(value) > 1:
                output[name] = self.process_metadata(name, value)
            else:
                output[name] = self.process_metadata(name, value[0])
        return output

    def read(self, source_path):
        """Parse content and metadata of markdown files"""
        
        with pelican_open(source_path) as text:
            lines = text.split('\n')

        meta = {}
        key = None
        if lines and BEGIN_RE.match(lines[0]):
            lines.pop(0)
        while lines:
            line = lines.pop(0)
            m1 = META_RE.match(line)
            if line.strip() == '' or END_RE.match(line):
                break  # blank line or end of YAML header - done
            if m1:
                key = m1.group('key').lower().strip()
                value = m1.group('value').strip()
                try:
                    meta[key].append(value)
                except KeyError:
                    meta[key] = [value]
            else:
                m2 = META_MORE_RE.match(line)
                if m2 and key:
                    # Add another line to existing key
                    meta[key].append(m2.group('value').strip())
                else:
                    lines.insert(0, line)
                    break  # no meta data - done

        metadata = self._parse_metadata(meta)
        content = '\n'.join(lines)

        m2μr = MicronRenderer()
        m2μ = Markdown(renderer=m2μr)
        m2μ.inline.register('underlined', UNDERLINED, parse_underlined, before='emphasis')
        m2μ.renderer.register('underlined', render_underlined_mu)
        content = m2μ(content)
        print(content)
        return content, metadata

# === M I C R O N   W R I T E R ===

class MicronWriter(Writer):
    
    def __init__(self, output_path, settings):
        super().__init__(output_path, settings)
        self.output_path = settings.get('MICRON_PATH', 'micron/')

    def write_file(self, name, template, context, relative_urls=False,
                   paginated=None, template_name=None, override_output=False,
                   url=None, **kwargs):
        template = template.environment.get_template( template.name.replace('.html', '.mu'))
        name = name.replace('.html', '.mu')
        if name is False or \
           name == "" or \
           not is_selected_for_writing(self.settings,
                                       os.path.join(self.output_path, name)):
            return
        elif not name:
            # other stuff, just return for now
            return

        def _write_file(template, localcontext, output_path, name, override):
            """Render the template write the file."""
            # set localsiteurl for context so that Contents can adjust links
            if localcontext['localsiteurl']:
                context['localsiteurl'] = localcontext['localsiteurl']
            output = template.render(localcontext)
            path = sanitised_join(output_path, name)

            try:
                os.makedirs(os.path.dirname(path))
            except Exception:
                pass

            with self._open_w(path, 'utf-8', override=override) as f:
                f.write(output)

            # Send a signal to say we're writing a file with some specific
            # local context.
            signals.content_written.send(path, context=localcontext)

        def _get_localcontext(context, name, kwargs, relative_urls):
            localcontext = context.copy()
            localcontext['localsiteurl'] = localcontext.get(
                'localsiteurl', None)
            if relative_urls:
                relative_url = path_to_url(get_relative_path(name))
                localcontext['SITEURL'] = relative_url
                localcontext['localsiteurl'] = relative_url
            localcontext['output_file'] = name
            localcontext.update(kwargs)
            return localcontext

        if paginated is None:
            paginated = {key: val for key, val in kwargs.items()
                         if key in {'articles', 'dates'}}

        # pagination
        if paginated and template_name in self.settings['PAGINATED_TEMPLATES']:
            # pagination needed
            per_page = self.settings['PAGINATED_TEMPLATES'][template_name] \
                or self.settings['DEFAULT_PAGINATION']

            # init paginators
            paginators = {key: Paginator(name, url, val, self.settings,
                                         per_page)
                          for key, val in paginated.items()}

            # generated pages, and write
            for page_num in range(list(paginators.values())[0].num_pages):
                paginated_kwargs = kwargs.copy()
                for key in paginators.keys():
                    paginator = paginators[key]
                    previous_page = paginator.page(page_num) \
                        if page_num > 0 else None
                    page = paginator.page(page_num + 1)
                    next_page = paginator.page(page_num + 2) \
                        if page_num + 1 < paginator.num_pages else None
                    paginated_kwargs.update(
                        {'%s_paginator' % key: paginator,
                         '%s_page' % key: page,
                         '%s_previous_page' % key: previous_page,
                         '%s_next_page' % key: next_page})

                localcontext = _get_localcontext(
                    context, page.save_as, paginated_kwargs, relative_urls)
                _write_file(template, localcontext, self.output_path,
                            page.save_as, override_output)
        else:
            # no pagination
            localcontext = _get_localcontext(
                context, name, kwargs, relative_urls)
            _write_file(template, localcontext, self.output_path, name,
                        override_output)

def add_reader(readers):
    readers.reader_classes['md'] = MarkdownToMicronReader

def add_writer(pelican_object):
    return MicronWriter

def register():
    signals.readers_init.connect(add_reader)
    signals.get_writer.connect(add_writer)