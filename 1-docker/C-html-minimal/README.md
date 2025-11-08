
# the files
## main.py

We are slowly trying to work towards showing a bit more frontend.
The first endpoints are similar to what we had before, but we are adding a few things

### async
Note we are using async functions. Essentially, this means that the server can handle multiple requests at the same time. When the function get_image is called, it might take some time to read the image from disk. If we would not use async, the server would be blocked until the image is read. With async, other requests can be handled in the meantime.

### HTMLResponse
We are returning HTML code directly from the endpoint. This is a simple way to get started with web pages. This can be improved a lot, for example by using templates, but this is out of scope for this course.

## Dockerfile
Because we need the png to show in the html, we want to copy the png file into the docker image.

## Makefile
An important new feature we are using in the makefile is to let the makefile check for the existence of an image file, and if the file isnt there, run some command (in this case, copy it from the parent folder)

Another feature we are using is to make the build command depend on the image file. This way, if the image file changes, the build will rerun, which will in turn copy the new image into the docker image.

# Exercise
- do not run `make build`, but directly run `make run`. Make sure you understand why this still works! Also check that the image is copied from the parent folder and an `img` folder is created here.
- check both endpoints with your browser.
- run `make clean` when you are done.


# More documentation

You can find more documentation about this setup on the [fastapi documentation](https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi)
