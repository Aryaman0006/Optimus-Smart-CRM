print("STARTING APP")

import os
import sys
from flask import Flask, request,redirect,render_template,send_file,session
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ---------------- LOAD DATA ----------------

# ---------------- LOAD DATA ----------------

if getattr(sys, 'frozen', False):
    BASE = sys._MEIPASS
else:
    BASE = os.path.dirname(
        os.path.abspath(__file__)
    )

csv_path = os.path.join(
    BASE,
    "data",
    "customers.csv"
)

# LOAD CSV FIRST
data = pd.read_csv(csv_path)
source_map = {
    "Website":0,
    "Instagram":1,
    "Referral":2,
    "LinkedIn":3
}

data['source_text'] = data['source']

data['source'] = data[
    'source'
].map(
    source_map
)

data['source'] = pd.to_numeric(
    data['source'],
    errors='coerce'
).fillna(0)

# phone as text
data['phone'] = data['phone'].astype(str)

# source conversion
source_map = {
    "Website":0,
    "Instagram":1,
    "Referral":2,
    "LinkedIn":3
}

data['source'] = data['source'].map(
    source_map
)

# numeric conversion
data['source'] = pd.to_numeric(
    data['source'],
    errors='coerce'
).fillna(0)

data['interest_level'] = pd.to_numeric(
    data['interest_level'],
    errors='coerce'
).fillna(0)

data['last_contact_days'] = pd.to_numeric(
    data['last_contact_days'],
    errors='coerce'
).fillna(0)

data['converted'] = pd.to_numeric(
    data['converted'],
    errors='coerce'
).fillna(0)

data = data.fillna(0)

app = Flask(
    __name__,

    template_folder=os.path.join(
        BASE,
        "templates"
    ),

    static_folder=os.path.join(
        BASE,
        "static"
    )
)
app.secret_key="optimus123"

# ---------------- ANALYTICS ----------------

def lead_score(row):

    score = 0

    # interest

    if row['interest_level'] == 2:
        score += 30

    elif row['interest_level'] == 1:
        score += 20

    else:
        score += 10

    # recency

    if row['last_contact_days'] <= 7:
        score += 25

    elif row['last_contact_days'] <= 30:
        score += 15

    else:
        score += 5

    # source

    if row['source'] == 2:
        score += 20

    elif row['source'] == 1:
        score += 10

    # converted

    if row['converted'] == 1:
        score += 15

    return score


def priority(score):

    if score >= 70:

        return "🔥 Hot"

    elif score >= 40:

        return "🟡 Warm"

    return "❄️ Cold"


def followup(days):

    if days > 7:
        return "⚠ Needs Follow-up"

    return "OK"
def recommendation(row):

    if (
        row['priority'] == "Hot"
        and
        row['last_contact_days'] > 7
    ):

        return "📞 Contact Now"

    elif (
        row['prediction'] == 1
    ):

        return "👀 Monitor"

    else:

        return "🧊 Low Priority"
    
@app.route('/login',methods=['GET','POST']
    )

def login():

    if request.method=='POST':

        username=request.form['username']

        password=request.form['password']

        if (
            username=="admin"
            and
            password=="1234"
        ):

            session[
            'user'
            ]=username

            return redirect('/')

    return render_template(
        'login.html'
    )


# ---------------- HOME ----------------

@app.route('/')

def home():

    if 'user' not in session:
        return redirect('/login')

    global data

    data = pd.read_csv(csv_path)

    search = request.args.get(
        'q',
        ''
    )

    if search:

        data = data[
            data.astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    search,
                    case=False
                ).any(),
                axis=1
            )
        ]

    data['phone'] = data['phone'].astype(str)

    data['source_text'] = data['source']

    source_map = {
        "Website":0,
        "Instagram":1,
        "Referral":2,
        "LinkedIn":3
    }

    data['source'] = data[
        'source'
    ].map(
        source_map
    )

    data['source'] = pd.to_numeric(
        data['source'],
        errors='coerce'
    ).fillna(0)

    data['interest_level'] = pd.to_numeric(
        data['interest_level'],
        errors='coerce'
    ).fillna(0)

    data['last_contact_days'] = pd.to_numeric(
        data['last_contact_days'],
        errors='coerce'
    ).fillna(0)

    data['converted'] = pd.to_numeric(
        data['converted'],
        errors='coerce'
    ).fillna(0)

    data = data.fillna(0)

    # analytics

    data['score'] = data.apply(
        lead_score,
        axis=1
    )

    data['priority'] = data[
        'score'
    ].apply(
        priority
    )

    data['follow_up'] = data[
        'last_contact_days'
    ].apply(
        followup
    )

    # segmentation

    features = data[
        [
            'interest_level',
            'last_contact_days',
            'score'
        ]
    ]

    if len(features) >= 3:

        kmeans = KMeans(
            n_clusters=3,
            random_state=42
        )

        data['segment'] = kmeans.fit_predict(
            features
        )

    else:

        data['segment'] = 0

    # prediction

    X = data[
        [
            'interest_level',
            'last_contact_days',
            'source'
        ]
    ]

    y = data['converted']

    if len(y.unique()) > 1:

        model = LogisticRegression()

        model.fit(
            X,
            y
        )

        data['prediction'] = model.predict(
            X
        )

        accuracy = accuracy_score(
            y,
            data['prediction']
        )

    else:

        data['prediction'] = 0

        accuracy = 0

    data['recommendation'] = data.apply(
        recommendation,
        axis=1
    )

    data = data.sort_values(
        'score',
        ascending=False
    )

    total = len(data)

    converted = len(
        data[
            data['converted']==1
        ]
    )

    hot = len(
        data[
            data['priority']=="🔥 Hot"
        ]
    )

    warm = len(
        data[
            data['priority']=="🟡 Warm"
        ]
    )

    cold = len(
        data[
            data['priority']=="❄️ Cold"
        ]
    )

    if total > 0:

        top_lead = data.iloc[0]

    else:

        top_lead = {
            'name':"None",
            'score':0,
            'recommendation':"-"
        }

    conversion_rate = (
        converted /
        total *
        100
    ) if total else 0

    source_stats = data[
        'source_text'
    ].value_counts().to_dict()

    city_stats = data[
        'city'
    ].value_counts().to_dict()

    interested = len(
        data[
            data['interest_level'] > 0
        ]
    )

    contacted = len(
        data[
            data['last_contact_days'] <= 7
        ]
    )

    data['actions'] = data.apply(

        lambda row:

        f"<a href='/edit/{row['customer_id']}'>✏ Edit</a><br><br><a href='/delete/{row['customer_id']}'>🗑 Delete</a>",

        axis=1
    )

    data['source'] = data[
        'source_text'
    ]

    table = data.to_html(
        classes='table',
        index=False,
        escape=False
    )

    return render_template(

        "home.html",

        source_stats=source_stats,

        city_stats=city_stats,

        interested=interested,

        contacted=contacted,

        table=table,

        total=total,

        converted=converted,

        hot=hot,

        warm=warm,

        cold=cold,

        accuracy=round(
            accuracy*100,
            2
        ),

        conversion_rate=round(
            conversion_rate,
            2
        ),

        top_lead=top_lead
    )

# ---------------- ADD ----------------#

@app.route('/add', methods=['GET', 'POST'])

def add():

    global data

    if request.method == 'POST':

        name = request.form['name']

        email = request.form['email']

        phone = request.form['phone']

        city = request.form['city']
         
        source = int(request.form['source'])

        interest_level = int(request.form['interest_level'])

        last_contact_days = int(request.form['last_contact_days'])

        converted = int(request.form['converted'])

        new_customer = {

            'customer_id':
            data['customer_id'].max() + 1,

            'name': name,

            'email': email,

            'phone': phone,

            'city': city,

            'source':source,

            'interest_level':interest_level,

            'last_contact_days':last_contact_days,

            'converted':converted

        }

        data = pd.concat(
            [
                data,
                pd.DataFrame(
                    [new_customer]
                )
            ],

            ignore_index=True
        )

        data.to_csv(
            csv_path,
            index=False
        )

        return redirect('/')

    return render_template(
        "add.html"
    )


# ---------------- EDIT ----------------

@app.route(
    '/edit/<int:customer_id>',
    methods=['GET', 'POST']
)

def edit(customer_id):

    global data

    data = pd.read_csv(
        csv_path
    )

    data['phone'] = data[
        'phone'
    ].astype(str)

    data = data.fillna(0)

    customer = data[
        data[
            'customer_id'
        ] == customer_id
    ].iloc[0]

    if request.method == 'POST':

        data.loc[
            data[
                'customer_id'
            ] == customer_id,
            'name'
        ] = request.form['name']

        data.loc[
            data[
                'customer_id'
            ] == customer_id,
            'email'
        ] = request.form['email']

        data.loc[
            data[
                'customer_id'
            ] == customer_id,
            'phone'
        ] = request.form['phone']

        data.loc[
            data[
                'customer_id'
            ] == customer_id,
            'city'
        ] = request.form['city']

        data.loc[
            data[
                'customer_id'
            ] == customer_id,
            'source'
        ] = int(
            request.form['source']
        )

        data.loc[
            data[
                'customer_id'
            ] == customer_id,
            'interest_level'
        ] = int(
            request.form[
                'interest_level'
            ]
        )

        data.loc[
            data[
                'customer_id'
            ] == customer_id,
            'last_contact_days'
        ] = int(
            request.form[
                'last_contact_days'
            ]
        )

        data.loc[
            data[
                'customer_id'
            ] == customer_id,
            'converted'
        ] = int(
            request.form[
                'converted'
            ]
        )

        data.to_csv(
            csv_path,
            index=False
        )

        return redirect('/')

    return render_template(
        "edit.html",
        customer=customer
    )


# ---------------- DELETE ----------------

@app.route(
'/delete/<int:customer_id>'
)

def delete(customer_id):

    global data

    data = pd.read_csv(
        csv_path
    )

    data['phone'] = data[
        'phone'
    ].astype(str)

    data = data[
        data[
            'customer_id'
        ] != customer_id
    ]

    data.to_csv(
        csv_path,
        index=False
    )

    return redirect('/')
# ---------------- EXPORT CSV ----------------

@app.route('/export')

def export_csv():

    export_folder = os.path.join(
        os.path.expanduser("~"),
        "Documents",
        "OptimusExports"
    )

    os.makedirs(
        export_folder,
        exist_ok=True
    )

    export_file = os.path.join(
        export_folder,
        "customers_export.csv"
    )

    data.to_csv(
        export_file,
        index=False
    )

    return send_file(
        export_file,
        as_attachment=True
    )

# ---------------- PDF REPORT ----------------

@app.route('/pdf')

def pdf_report():

    if getattr(sys, 'frozen', False):

        pdf_folder = os.path.join(
            os.path.expanduser("~"),
            "Documents",
            "OptimusExports"
        )

        os.makedirs(
            pdf_folder,
            exist_ok=True
        )

        pdf_file = os.path.join(
            pdf_folder,
            "optimus_report.pdf"
        )

    else:

        pdf_file = "optimus_report.pdf"

    data = pd.read_csv(
        csv_path
    )

    data['score'] = data.apply(
        lead_score,
        axis=1
    )

    data['priority'] = data[
        'score'
    ].apply(
        priority
    )

    total = len(data)

    converted = len(
        data[
            data['converted'] == 1
        ]
    )

    hot = len(
        data[
            data['priority'] == "🔥 Hot"
        ]
    )

    warm = len(
        data[
            data['priority'] == "🟡 Warm"
        ]
    )

    cold = len(
        data[
            data['priority'] == "❄️ Cold"
        ]
    )

    doc = SimpleDocTemplate(
        pdf_file
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>OPTIMUS SMART CRM REPORT</b>",
            styles['Title']
        )
    )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Paragraph(
            f"Total Leads : {total}",
            styles['BodyText']
        )
    )

    story.append(
        Paragraph(
            f"Converted : {converted}",
            styles['BodyText']
        )
    )

    story.append(
        Paragraph(
            f"Hot : {hot}",
            styles['BodyText']
        )
    )

    story.append(
        Paragraph(
            f"Warm : {warm}",
            styles['BodyText']
        )
    )

    story.append(
        Paragraph(
            f"Cold : {cold}",
            styles['BodyText']
        )
    )

    doc.build(story)

    return send_file(
        pdf_file,
        as_attachment=True
    )
# ---------------- LOGOUT ----------------

@app.route('/logout')

def logout():

    session.clear()

    return redirect(
        '/login'
    )
# ---------------- RUN ----------------

if __name__ == '__main__':

    app.run(
        debug=True
    )