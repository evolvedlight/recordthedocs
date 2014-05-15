# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required
import docutils.core

blueprint = Blueprint("project", __name__, url_prefix='/project',
                        static_folder="../static")


@blueprint.route("/<path:repo_url>")
def whole_project(repo_url):
    
    real_repo_url = get_real_repo_url(repo_url)
    
    from gittle import Gittle
    
    repo_path = '/tmp/gittle_bare'
    repo = Gittle(repo_path)
    with open('%s/docs/index.rst' % repo_path, 'r') as index_page:
        file_content = index_page.read()
    initial_content = rst2html(file_content)
    #except:
    #    repo = Gittle.clone(repo_url, repo_path)
    return render_template("project/home.html", 
        repo_url=repo_url, 
        repo=repo, 
        initial_content=initial_content
    )
    
def rst2html(rst_content):
    
    content = surround_toctree(rst_content)
    return content

def surround_toctree(content):
    output = ""
    in_toctree = False;
    for line in content.split('\n'):
        if line.startswith('.. '):
            print "Entering toctree section"
            in_toctree = True
            output = output + '<div class="literalrst">'
            output = output + line
        elif in_toctree and line == "":
            print "Exiting toctree secion at line %s"% line
            in_toctree = False
            output = output + line + '</div>'
        elif in_toctree:
            output = output + line
        else:
            if line:
                print "Passing to docutils:"
                print line
                
                output = output + docutils.core.publish_parts(line, writer_name="html")['html_body']
    return output
    
def get_real_repo_url(repo_url):
    if repo_url.startswith('http://'):
        return repo_url
    return "http://%s" % repo_url