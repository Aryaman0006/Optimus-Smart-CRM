function exportCSV(){

let table=
document.querySelector(
"table"
)

let csv=[]

for(
let row of table.rows
){

let cols=[]

for(
let cell of row.cells
){

cols.push(
cell.innerText
)

}

csv.push(
cols.join(",")
)

}

let blob=
new Blob(
[csv.join("\n")],
{
type:
"text/csv"
}
)

let a=
document.createElement(
"a"
)

a.href=
URL.createObjectURL(
blob
)

a.download=
"optimus_leads.csv"

a.click()

}