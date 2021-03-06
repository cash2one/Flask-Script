# coding=utf-8
"""
视图修饰器，需要放置在route下方
"""
from functools import wraps
from flask import Response, render_template, request, current_app

__author__ = 'GaoJie'


def responsed(f):
    """
    为请求答复自动添加response_class()
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if isinstance(result, Response):
                return result
        except Exception as e:
            current_app.logger.exception(e)
        finally:
            return current_app.response_class()
    return decorated


def templated(template=None):
    """
    模板修饰器，视图返回dict给模板
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint.replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def action(action_list, name=None):
    """
    加入当前环境执行列表
    name应该和route一致，如果route和fun一致，则为空即可
    """
    def decorator(f):
        action_list.append(f.__name__ if not name else name)

        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator