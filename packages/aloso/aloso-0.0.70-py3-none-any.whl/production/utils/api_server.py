import uvicorn

import config

if __name__ == '__main__':
    uvicorn.run("api.server.main:app", host='localhost', port=8005, reload=True, reload_includes=config.root_dir)
