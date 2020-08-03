const fetch = require("node-fetch");

async function p() {

   let f = await (await fetch('https://randomuser.me/api/')).json()
   return f
} 

async function ko() {
    let m = await p()
    console.log(m)

}

ko()

