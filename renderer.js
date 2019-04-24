const zerorpc = require("zerorpc")
let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")

let address = document.querySelector('#address')
let result = document.querySelector('#result')
address.addEventListener('input', () => {
  client.invoke("scanAddress", address.value, (error, res) => {
    if(error) {
      console.error(error)
    } else {
      result.textContent = res
    }
  })
})
address.dispatchEvent(new Event('input'))
