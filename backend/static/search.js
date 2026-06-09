document
.getElementById(
"searchBox"
)

.addEventListener(
"keyup",

function(){

let value=
this.value
.toLowerCase()

let rows=
document.querySelectorAll(
"tbody tr"
)

rows.forEach(
row=>{

row.style.display=

row.innerText
.toLowerCase()
.includes(
value
)

? ""

: "none"

})

})