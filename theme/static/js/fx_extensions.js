document.addEventListener("fx:init", (evt) => {
    let trigger = evt.target.getAttribute("fx-trigger")
    if(trigger === "intersect") {
        let obs = evt.target.__fixi_ob = new IntersectionObserver((entries)=>{
            for(const entry of entries) {
                if (entry.isIntersecting){
                    obs.unobserve(evt.target)
                    evt.target.__fixi_ob = null;
                    evt.target.dispatchEvent(new CustomEvent("intersect"))
                    return;
                }
            }
        })
        obs.observe(evt.target)
    }
})
