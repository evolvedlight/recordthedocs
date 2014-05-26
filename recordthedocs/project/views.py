# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required
import docutils.core
from docutils.core import publish_string, publish_doctree, publish_parts, Publisher
from docutils import frontend, io

blueprint = Blueprint("project", __name__, url_prefix='/project',
                        static_folder="../static")


@blueprint.route("/<path:repo_url>")
def whole_project(repo_url):
    
    real_repo_url = get_real_repo_url(repo_url)
    
    from gittle import Gittle
    
    try:
        repo_path = '/tmp/gittle_bare'
        repo = Gittle(repo_path)
    except: 
        repo = Gittle.clone(repo_url, repo_path)
    with open('%s/docs/index.rst' % repo_path, 'r') as index_page:
        file_content = index_page.read()
    initial_content = rst2html(file_content)
    #except:
    #    
    return render_template("project/home.html", 
        repo_url=repo_url, 
        repo=repo, 
        initial_content=initial_content,
        page_title="index.rst"
    )
    
    
default_rst_opts = {
    'no_generator': True,
    'no_source_link': True,
    'tab_width': 4,
    'file_insertion_enabled': False,
    'raw_enabled': False,
    'stylesheet_path': None,
    'traceback': True,
    'halt_level': 5,
    'toc_backlinks': None,
    'traceback': None,
    'debug': None,
    #'input_encoding_error_handler': 'ignore',
    #'output_encoding_error_handler': 'ignore',
    'report_level': 1,
}
    
def rst2html(rst, theme=None, opts=None):
    rst_opts = default_rst_opts.copy()
    # if opts:
    #     rst_opts.update(opts)
    # rst_opts['template'] = 'var/themes/template.txt'

    # stylesheets = ['basic.css']
    # if theme:
    #     stylesheets.append('%s/%s.css' % (theme, theme))
    # rst_opts['stylesheet'] = ','.join([J('var/themes/', p) for p in stylesheets ])
    
    halfway = publish_doctree(rst)
    for node in halfway.traverse():
        if node.tagname == "system_message":
            new_strng = ''.join([x.rawsource for x in node.children])
            if new_strng:
                new_element = docutils.nodes.literal_block(new_strng, new_strng)
                node.parent.replace(node, new_element)
            else:
                node.parent.remove(node)
            
    #out = publish_string(rst, writer_name='html', settings_overrides=rst_opts)
    out = publish_from_doctree_parts(halfway, writer_name='html', settings_overrides=rst_opts)
    return out['html_body']

def publish_from_doctree_parts(document, destination_path=None,
                     writer=None, writer_name='pseudoxml',
                     settings=None, settings_spec=None,
                     settings_overrides=None, config_section=None,
                     enable_exit_status=False):
    """
    Set up & run a `Publisher` to render from an existing document
    tree data structure, for programmatic use with string I/O.  Return
    the encoded string output.
     
    Note that document.settings is overridden; if you want to use the settings
    of the original `document`, pass settings=document.settings.
     
    Also, new document.transformer and document.reporter objects are
    generated.
     
    For encoded string output, be sure to set the 'output_encoding' setting to
    the desired encoding.  Set it to 'unicode' for unencoded Unicode string
    output.  Here's one way::
     
        publish_from_doctree(
            ..., settings_overrides={'output_encoding': 'unicode'})
     
    Parameters: `document` is a `docutils.nodes.document` object, an existing
    document tree.
     
    Other parameters: see `publish_programmatically`.
    """
    reader = docutils.readers.doctree.Reader(parser_name='null')
    pub = Publisher(reader, None, writer,
                    source=io.DocTreeInput(document),
                    destination_class=io.StringOutput, settings=settings)
    if not writer and writer_name:
        pub.set_writer(writer_name)
    pub.process_programmatic_settings(
        settings_spec, settings_overrides, config_section)
    pub.set_destination(None, destination_path)
    pub.publish(enable_exit_status=enable_exit_status)
    return pub.writer.parts
    
def get_real_repo_url(repo_url):
    if repo_url.startswith('http://'):
        return repo_url
    return "http://%s" % repo_url