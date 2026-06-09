document
.querySelectorAll(
".card p"
)

.forEach(
counter=>{

let target=
parseInt(
counter.innerText
)

let value=0

let interval=
setInterval(

()=>{

value++

counter.innerText=
value

if(
value>=target
)

clearInterval(
interval)

},

40

)

}
)