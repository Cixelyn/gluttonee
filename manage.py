from werkzeug import script

def __make_app():
  from gluttonee import app
  return app

def __make_shell():
  app = __make_app()

  ctx = app.test_request_context()
  ctx.push()
  app.preprocess_request()

  import flask

  return locals()

def __map_app():
  app = __make_app()
  print "Routing Map: \n"+str(app.url_map)

action_map = __map_app
action_serve = script.make_runserver(__make_app, use_reloader=True,
        use_debugger=True)
action_console = script.make_shell(__make_shell)
script.run()


