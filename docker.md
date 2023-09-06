## Pull and Run Our Docker Image
**coming soon . . .**

## Build and Run a Local Docker Image (based on the latest code)

Assuming you have Docker installed, with it's daemon running . . .
```bash
git clone https://github.com/NSSAC/PEpiTA.git
cd PEpiTA
# Build an image, assigning the following name and tag ("<name>:<tag>").
docker build --tag pepita:001 .
```

Create a container and run with the default "[CMD]" using the default "[ENTRYPOINT],
exposing your host machine('s browser) to the contained web server's port."
(see the [Dockerfile](Dockerfile)).

```bash
docker run --interactive --tty --publish 8000:8000  pepita:001
```

That should sit "blocking" your terminal. You should now be able to
connect to the web application from [localhost:8000](http://localhost:8000).
Use Cmd-C or Ctl-C at the terminal to kill the server.

## Cleanup

To clean up any containers . . .
```bash
docker ps --all # list all containers, including NAMEs (right most column)
docker rm <NAME>
```

To clean up any images, e.g. . . .

```bash
docker image list # see what you have
docker image rm pepita:001
```

Fully clean house (remove all containers and images), if you want to.
```bash
docker rm --force $(docker ps --all --quiet) # containers
docker image prune --all --force             # images
```