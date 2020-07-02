import os

from bottle import response, static_file

from file_handler.handle_file import return_file, file_mime_type
from helper import Http_error
from log import LogMsg, logger
from messages import Message
from helper import dir_path


def js_serve(filename,username=None):

    save_path = '{}/statics/js'.format(dir_path)
    return serve_file(filename,save_path)

def css_serve(filename,username=None):
    save_path = '{}/statics/css'.format(dir_path)
    return serve_file(filename, save_path,"text/css")

def fonts_serve(filename,username=None):

    save_path = '{}/statics/fonts'.format(dir_path)
    return serve_file(filename,save_path)

def images_serve(filename,username=None):
    save_path = '{}/statics/images'.format(dir_path)
    return serve_file(filename,save_path)

def html_serve(filename,username=None):

    save_path = '{}/statics'.format(dir_path)
    return serve_file(filename,save_path)

def serve_file(filename,save_path, mime=None):
    try:
        file_path = '{}/{}'.format(save_path, filename)

        if os.path.isfile(file_path):
            response.content_type = file_mime_type(file_path)
        else:
            logger.debug(LogMsg.NOT_FOUND, file_path)
        if mime is None:
            response.body = static_file(filename, root=save_path, mimetype=response.content_type)
        else:
            response.content_type=mime
            response.body = static_file(filename, root=save_path, mimetype=mime)

        return response

    except:
        logger.exception(LogMsg.NOT_FOUND, exc_info=True)
        raise Http_error(404, Message.NOT_FOUND)