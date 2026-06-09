new Chart(

document.getElementById(
"cityChart"
),

{

type:"bar",

data:{

labels:

Object.keys(
cityStats
),

datasets:[{

label:"Leads",

data:

Object.values(
cityStats
),

backgroundColor:

"#7c3aed",

borderRadius:12

}]

}

}

)



new Chart(

document.getElementById(
"priorityChart"
),

{

type:"doughnut",

data:{

labels:[

"🔥 Hot",

"🟡 Warm",

"❄ Cold"

],

datasets:[{

data:[

hot || 1,

warm || 1,

cold || 1

],

backgroundColor:[

"#ff4d6d",

"#ffb703",

"#4cc9f0"

],

borderWidth:4,

hoverOffset:20

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

cutout:"55%",

plugins:{

legend:{

position:"top",

labels:{

color:"white",

font:{

size:14

}

}

}

}

}

}

)