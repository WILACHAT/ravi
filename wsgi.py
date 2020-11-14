import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, Markup
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from flask_basicauth import BasicAuth
import json
#import datetime
from datetime import datetime, timedelta






# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["BASIC_AUTH_USERNAME"] = "ravi"
app.config["BASIC_AUTH_PASSWORD"] = "melon"

basic_auth = BasicAuth(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ravi_mellon.db")



# Make sure API key is set


@app.route("/assumption", methods=["GET", "POST"])

def assumption():
    today = date.today()
    itemsassumption = []
    showalltoday = today.strftime("%B %d, %Y")
    select_assumpt = db.execute("SELECT * FROM assumption")
    counter = 0
    for row in select_assumpt:
        assumptionname = select_assumpt[counter]["assumption_name"]
        items = dict(assumptionname = assumptionname)
        itemsassumption.append(items)
        counter+=1
#if click on an assumption it will get variables from the database and display it if not then shows nothing
    if request.method == "POST":
        if request.form["action"] == "rong":
            action = request.form.get("hiddenrong")
            assumptionname = action
            assumption = db.execute("SELECT * FROM assumption WHERE assumption_name = :action", action = action)
            session["assumptionkey"] = assumption[0]["assumptionkey"]
            session["assumption_name"] = assumption[0]["assumption_name"]
            seedspeciesname = assumption[0]["seedspeciesname_ass"]
            startdate = assumption[0]["startdate_ass"]
            longtoong = assumption[0]["longtoong_ass"]
            medicine = assumption[0]["medicine_ass"]
            fb = assumption[0]["fb_ass"]
            sb = assumption[0]["sb_ass"]
            fhfb = assumption[0]["fhfb_ass"]
            shfb = assumption[0]["shfb_ass"]
            fhsb = assumption[0]["fhsb_ass"]
            shsb = assumption[0]["shsb_ass"]
            thsb = assumption[0]["thsb_ass"]
            ratiofhfb = assumption[0]["ratiofhfb_ass"]
            ratioshfb = assumption[0]["ratioshfb_ass"]
            ratiofhsb = assumption[0]["ratiofhsb_ass"]
            ratioshsb = assumption[0]["ratioshsb_ass"]
            ratiothsb = assumption[0]["ratiothsb_ass"]

            notefhfb = assumption[0]["note_fhfb_ass"]
            noteshfb = assumption[0]["note_shfb_ass"]
            notefhsb = assumption[0]["note_fhsb_ass"]
            noteshsb = assumption[0]["note_shsb_ass"]
            notethsb = assumption[0]["note_thsb_ass"]

            itemsddseedspecies = [None]
            itemsmedicinedd = [None]
            itemsselectmed = []
            seedddspecies = db.execute("SELECT seedspecies_id, seedspecies_name FROM seedspecies WHERE booleanseedspecies = 1")
            ptbdd = db.execute("SELECT ptb_id, ratiomed FROM ptb WHERE booleanptb = 1")
            medicinedd = db.execute("SELECT medicine_id, medicine_name FROM medicine WHERE booleanmedicine = 1")
            counter = 0
#GET LIST FOR DROPDOWN
            for row in seedddspecies:
                seedddspeciess = seedddspecies[counter]["seedspecies_name"]
                optionseedspeciesid = seedddspecies[counter]["seedspecies_id"]
                itemsrow = dict(seedddspeciess = seedddspeciess, optionseedspeciesid = optionseedspeciesid)
                itemsddseedspecies.append(itemsrow)
                counter+=1
            counter = 0


            counter = 0
            for row in medicinedd:
                medicineddd = medicinedd[counter]["medicine_name"]
                optionmedicineid = medicinedd[counter]["medicine_id"]
                itemsrow = dict(medicineddd = medicineddd, optionmedicineid = optionmedicineid)
                itemsmedicinedd.append(itemsrow)
                counter+=1

            selectmed = assumption[0]["medicine_ass"]
            selectmed = selectmed.split("'")
            for i in selectmed:
                med = i
                ye = dict(med = med)
                itemsselectmed.append(ye)


            return render_template("newassumption.html", assumptionname = assumptionname, seedspeciesname = seedspeciesname, startdate = startdate, longtoong = longtoong,
            medicine = medicine, fb = fb, sb = sb, fhfb = fhfb, shfb = shfb, fhsb = fhsb, shsb = shsb, thsb = thsb, ratiofhfb = ratiofhfb, ratioshfb = ratioshfb, ratiofhsb = ratiofhsb, ratioshsb = ratioshsb,
            ratiothsb = ratiothsb, notefhfb = notefhfb, noteshfb = noteshfb, notefhsb = notefhsb,
            noteshsb = noteshsb, notethsb = notethsb,  itemsddseedspecies = itemsddseedspecies,itemsmedicinedd = itemsmedicinedd, itemsselectmed = itemsselectmed)

    return render_template("assumption.html", today = showalltoday, itemsassumption = itemsassumption)
@app.route("/newassumption", methods=["GET", "POST"])
def newassumption():
    itemsddseedspecies = [None]
    itemsmedicinedd = [None]
    willy = 0
    seedddspecies = db.execute("SELECT seedspecies_id, seedspecies_name FROM seedspecies WHERE booleanseedspecies = 1")
    ptbdd = db.execute("SELECT ptb_id, ratiomed FROM ptb WHERE booleanptb = 1")
    medicinedd = db.execute("SELECT medicine_id, medicine_name FROM medicine WHERE booleanmedicine = 1")
    counter = 0

#SELECTING LISTS FOR DROP DOWN
    for row in seedddspecies:
        seedddspeciess = seedddspecies[counter]["seedspecies_name"]
        optionseedspeciesid = seedddspecies[counter]["seedspecies_id"]
        itemsrow = dict(seedddspeciess = seedddspeciess, optionseedspeciesid = optionseedspeciesid)
        itemsddseedspecies.append(itemsrow)
        counter+=1

    counter = 0
    for row in medicinedd:
        medicineddd = medicinedd[counter]["medicine_name"]
        optionmedicineid = medicinedd[counter]["medicine_id"]
        itemsrow = dict(medicineddd = medicineddd, optionmedicineid = optionmedicineid)
        itemsmedicinedd.append(itemsrow)
        counter+=1
#if user select save in assumption it tries to get value and then save to the database
    if request.content_type == "application/json":
        if 'id' in request.json.keys():

            forselectss = request.json['id']

            secondblock = db.execute("SELECT * FROM seedspecies WHERE seedspecies_id = :forselectss", forselectss = forselectss)
            secondblockk = secondblock[0]["secondblocknumdays"]
            seedspecies = secondblock[0]["seedspecies_id"]
            return ({'id':secondblockk, 'seedspecies': seedspecies}, 200, {'ContentType':'application/json'})
        if 'id' not in request.json.keys():

            fb = request.json['fb']
            sb = request.json['sb']
            seedspeciesname = request.json['ssname']
            assumptionname = request.json['assumptionname']
            itemsselectmed = request.json['itemsselectmed']
            longtoongdays = request.json['longtoongdays']
            fhfb =  request.json['fhfb']
            shfb =  request.json['shfb']
            fhsb =  request.json['fhsb']
            shsb =  request.json['shsb']
            thsb =  request.json['thsb']
            notefhfb =  request.json['notefhfb']
            noteshfb =  request.json['noteshfb']
            notefhsb =  request.json['notefhsb']
            noteshsb =  request.json['noteshsb']
            notethsb =  request.json['notethsb']
            ratiofhfb =  request.json['ratiofhfb']
            ratioshfb =  request.json['ratioshfb']
            ratiofhsb =  request.json['ratiofhsb']
            ratioshsb =  request.json['ratioshsb']
            ratiothsb =  request.json['ratiothsb']
            checkforsave = request.json['checkforsave']
            print(f"checkifsuccess: {checkforsave}")

            db.execute("INSERT INTO assumption (seedspeciesname_ass,startdate_ass,longtoong_ass,medicine_ass,fb_ass,sb_ass,fhfb_ass,shfb_ass,fhsb_ass,shsb_ass,thsb_ass,ratiofhfb_ass,ratioshfb_ass,ratiofhsb_ass,ratioshsb_ass,ratiothsb_ass,note_fhfb_ass,note_shfb_ass,note_fhsb_ass,note_shsb_ass,note_thsb_ass,assumption_name) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", seedspeciesname, "waan",longtoongdays,itemsselectmed,fb,sb,fhfb,shfb,fhsb,shsb,thsb,ratiofhfb,ratioshfb,ratiofhsb,ratioshsb,ratiothsb,notefhfb,noteshfb,notefhsb, noteshsb, notethsb, assumptionname)
            print(f"checkifsuccess2: {checkforsave}")
            return ({'checkforsave':checkforsave}, 200, {'ContentType':'application/json'})
          #  willy = 1
          #  flash("it is saved")
            #return redirect('assumption')
            #print(f"willy:{willy}")
            #print(f"willy: {willy}")
           # flash(Markup('Successfully registered, please click <a href="/newassumption" class="alert-link">here</a>'))

           # print("waaaaaaaaaaaaaaan")
            #return render_template("newassumption.html", willy = willy)

           #return ({'willy':willy} ,200, {'ContentType':'application/json'})


    return render_template("newassumption.html",itemsmedicinedd = itemsmedicinedd, itemsddseedspecies = itemsddseedspecies)

@app.route("/", methods=["GET","POST"])
@basic_auth.required
def index():
    """Show portfolio of stocks"""
#100% SELECTING value from database and displaying it in today
    today = date.today()
    showalltoday = today.strftime("%B %d, %Y")
    newstartdate = today.strftime("%Y-%m-%d")

    wetrythistogether = db.execute("SELECT * FROM rong JOIN session ON session.rong_id = rong.rong_id JOIN section ON section.session_id = session.session_id JOIN calendar ON calendar.section_id = section.section_id WHERE date = :newstartdate AND sessionstatus = 1",newstartdate = newstartdate)
    counter = 0
    itemsrowtoday = []
    itemsrowsstoday = []
    itemsmedmed = []
#EACH RONG IS ROW
    for row in wetrythistogether:

        wsectionid = wetrythistogether[counter]["section_id"]
        tryingsection = db.execute("SELECT * FROM calendar WHERE section_id = :wsection_id", wsection_id = wsectionid )

        newcounter = 0

        rongtoday = wetrythistogether[counter]["rong_id"]
        todaylm = wetrythistogether[counter]["litermellon"]
        rongcapacity = wetrythistogether[counter]["rong_capacity"]
        sectionid = wetrythistogether[counter]["section_id"]
        todayro = wetrythistogether[counter]["ratio_ones"]
        todayrh = wetrythistogether[counter]["ratio_hundreth"]
        todayr = wetrythistogether[counter]["ratio"]
        todaylpd = wetrythistogether[counter]["literperday"]
        eccalendar = wetrythistogether[counter]["eccalendar"]
        capacity = wetrythistogether[counter]["capacity"]
        todaysn = wetrythistogether[counter]["sessionname"]
        todayss = wetrythistogether[counter]["seedspecies_id"]
        seedspeciesname = db.execute("SELECT * FROM seedspecies WHERE seedspecies_id = :todayss", todayss = todayss)
        seedspeciesnamee = seedspeciesname[0]["seedspecies_name"]
        selectmed = wetrythistogether[counter]["medicinesession"]
        selectmed = selectmed.split("'")
        itemsselectmed = []
        for i in selectmed:
            med = i
            ye = dict(med = med)
            itemsselectmed.append(ye)
        todayrong = wetrythistogether[counter]["rong_name"]
        selectptb = wetrythistogether[counter]["ratiomedptb"]
        if selectptb == None:
            selectptb = "None"
        daynote = wetrythistogether[counter]["daynote"]
        if daynote == None:
            daynote = "None"
        medicinecalcalo = wetrythistogether[counter]["medicinecal"]
        if medicinecalcalo == None:
            medicinecalcal = ""
            dictjumpen = {"waan":1 }
            medicinecalcal = dictjumpen
        else:
            medicinecalcal = json.loads(medicinecalcalo)

        counter+=1
        itemsthisrow = dict(todaylm = todaylm, todayro = todayro, todayrh = todayrh, todayr = todayr, todaylpd = todaylpd, todaysn = todaysn, todayrong = todayrong, seedspeciesnamee = seedspeciesnamee, rongcapacity = rongcapacity, selectptb = selectptb, daynote = daynote, medicinecalcal = medicinecalcal, itemsselectmed = itemsselectmed, eccalendar = eccalendar, capacity = capacity)
        itemsrowtoday.append(itemsthisrow)
        itemsmed = dict(itemsselectmed = itemsselectmed)
        itemsmedmed.append(itemsmed)





    return render_template("ravilayout.html", today = showalltoday, itemsrowtoday = itemsrowtoday, itemsmedmed = itemsmedmed)
@app.route("/rong", methods=["GET","POST"])
def rong():
    items = []
    counter = 0
    rongs = db.execute("SELECT * FROM rong")

    for row in rongs:
        rongname = rongs[counter]["rong_name"]
        rongidd = rongs[counter]["rong_id"]
        counter+=1
        selectsessionn = db.execute("SELECT MAX(session_id) AS session_id, sessionstatus FROM session WHERE rong_id = :rongidd", rongidd = rongidd)
        checkifsuccess = selectsessionn[0]["sessionstatus"]
        if selectsessionn[0]["session_id"] == None:
            checkifsuccess = 0
        itemsrow = dict(rongname = rongname, checkifsuccess = checkifsuccess)
        items.append(itemsrow)
    if request.method == "POST":
#getting rong name to display
        if request.form["action"] == "rong":
            action = request.form.get("hiddenrong")
            rongname = action
            rongid= db.execute("SELECT * FROM rong WHERE rong_name = :action", action = action)
            session["rongg_id"] = rongid[0]["rong_id"]
            session["rongg_name"] = rongid[0]["rong_name"]
            rong_id = session["rongg_id"]

            today = date.today()
            newstartdate = today.strftime("%Y-%m-%d")
            selectsession = db.execute("SELECT MAX(session_id) AS session_id, seedspecies_id,sessionname,medicinesession,beforelongtoong,assumption_val FROM session WHERE rong_id = :rong_id", rong_id = rong_id)
#all of this checks in 4choices if it is avaliable (any ongoing session etc)
            checkifsuccess = 0
            checkforcurrenttable = 0
            checkforhistory = 0
            waan = selectsession[0]["session_id"]

            if selectsession[0]["session_id"] != None:
                session_id = selectsession[0]["session_id"]
                electsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)
                section_id5 = electsection[5]["section_id"]

                selectstartdate5 = db.execute("SELECT * FROM calendar WHERE section_id = :section_id", section_id = section_id5)

                laststartdate = selectstartdate5[-1]["date"]
                print(f"this is the last startdate of current or something: {laststartdate}")

                if laststartdate > newstartdate:
                    oreo = "yummy"
                else:
                    sessionstatus = 0
                    db.execute("UPDATE session SET sessionstatus = :sessionstatus WHERE rong_id = :rong_id ORDER BY session_id DESC LIMIT 1",sessionstatus = sessionstatus, rong_id = rong_id )

            selectsessionn = db.execute("SELECT MAX(session_id) AS session_id, sessionstatus FROM session WHERE rong_id = :rong_id", rong_id = rong_id)
            checkifsuccess = selectsessionn[0]["sessionstatus"]
            checkforcurrenttable = selectsessionn[0]["sessionstatus"]
            checkforhistory = 1


            if selectsession[0]["session_id"] == None:
                checkifsuccess = 0
                checkforcurrenttable = 0
                checkforhistory = 0
                checkforchange = 0




            return render_template("4choices.html", rongname = rongname, checkifsuccess = checkifsuccess, checkforcurrenttable = checkforcurrenttable, checkforhistory = checkforhistory)

    return render_template("rong.html", items = items)


@app.route("/4choices", methods=["GET", "POST"])
def fourchoices():
    print("choices!!!")
    items=[]
    counter = 0
    checkifsuccess = 0
    checkforcurrenttable = 0
    checkforhistory = 0
#getting ronngame from session
    rongname = session["rongg_name"]
    rong_id = session["rongg_id"]
    if request.method == "POST":
        print("yeeeeeeee")
        selectsession = db.execute("SELECT MAX(session_id) AS session_id, seedspecies_id,sessionname,medicinesession,beforelongtoong,assumption_val FROM session WHERE rong_id = :rong_id", rong_id = rong_id)
        sessionstatus = 0
       # select * from session order by session_id desc limit 1 where rong_id = 2;
        db.execute("UPDATE session SET sessionstatus = :sessionstatus WHERE rong_id = :rong_id ORDER BY session_id DESC LIMIT 1",sessionstatus = sessionstatus, rong_id = rong_id )
        #sessionno = db.execute("UPDATE session SET seedspecies_id = :seedspeciesrealid, firstblocknumdays = :fb, rong_id = :rong_id, sessionname = :sessionname, medicinesession = :selectmed, beforelongtoong = :longtoongdays, assumption_val = :assumption_val WHERE session_id = :session_id", seedspeciesrealid = seedspeciesrealid, fb = fb, rong_id = rong_id, sessionname = sessionname,selectmed = selectmed ,longtoongdays = longtoongdays, assumption_val = assumption_val, session_id = session_id)

        checkifsuccess = 0
        checkforcurrenttable = 0
        checkforhistory = 0
        return render_template("4choices.html", rongname = rongname, checkifsuccess = checkifsuccess, checkforcurrenttable = checkforcurrenttable, checkforhistory = checkforhistory)



    today = date.today()
    newstartdate = today.strftime("%Y-%m-%d")
    selectsession = db.execute("SELECT MAX(session_id) AS session_id, seedspecies_id,sessionname,medicinesession,beforelongtoong,assumption_val FROM session WHERE rong_id = :rong_id", rong_id = rong_id)
#all of this checks in 4choices if it is avaliable (any ongoing session etc)

    waan = selectsession[0]["session_id"]


    if selectsession[0]["session_id"] != None:
        session_id = selectsession[0]["session_id"]
        electsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)
        section_id5 = electsection[5]["section_id"]

        selectstartdate5 = db.execute("SELECT * FROM calendar WHERE section_id = :section_id", section_id = section_id5)

        laststartdate = selectstartdate5[-1]["date"]
        print(f"this is the last startdate of current or something: {laststartdate}")

        if laststartdate > newstartdate:
            oreo = "yummy"
        else:
            sessionstatus = 0
            db.execute("UPDATE session SET sessionstatus = :sessionstatus WHERE rong_id = :rong_id ORDER BY session_id DESC LIMIT 1",sessionstatus = sessionstatus, rong_id = rong_id )

    selectsessionn = db.execute("SELECT MAX(session_id) AS session_id, sessionstatus FROM session WHERE rong_id = :rong_id", rong_id = rong_id)
    checkifsuccess = selectsessionn[0]["sessionstatus"]
    checkforcurrenttable = selectsessionn[0]["sessionstatus"]
    checkforhistory = 1


    if selectsession[0]["session_id"] == None:
        checkifsuccess = 0
        checkforcurrenttable = 0
        checkforhistory = 0
        checkforhistory = 0


    print("This is before render_template")
    return render_template("4choices.html", rongname = rongname, checkifsuccess = checkifsuccess, checkforcurrenttable = checkforcurrenttable, checkforhistory = checkforhistory)



@app.route("/historyselect", methods=["GET", "POST"])
def historyselect():
    rong_id = session["rongg_id"]
    allsession = db.execute("SELECT * FROM session  WHERE rong_id = :rong_id AND sessionstatus = 0", rong_id = rong_id)
    itemssessionnum = []
    itemscalendarfhfb = []
    itemscalendarshfb = []
    itemscalendarfhsb = []
    itemscalendarshsb = []
    itemscalendarthsb = []
    itemssection = []
    itemsselectallptb = [None]
    rongg = db.execute("SELECT * FROM rong WHERE rong_id = :rong_id", rong_id = rong_id)
    capacityrong = rongg[0]["rong_capacity"]
    rongname = rongg[0]["rong_name"]

    counter = 0
    for row in allsession:
        sessionname = allsession[counter]["sessionname"]
        session_id = allsession[counter]["session_id"]
        itemsrowsession = dict(sessionname = sessionname, session_id = session_id)
        itemssessionnum.append(itemsrowsession)
        counter+=1

#if something is selected on history get variable like current table but for that table
        if request.method == "POST":
            if request.form["action"] == "rong":
                action = request.form.get("hiddenrong")
                rongname = action
                selecthissession= db.execute("SELECT * FROM session WHERE session_id = :action", action = action)
                session["sessionname"] = selecthissession[0]["sessionname"]
                session["session_id"] = selecthissession[0]["session_id"]
                sessionname = session["sessionname"]

                selectsession = db.execute("SELECT * FROM session WHERE session.session_id = :action", action = action)
                allnotes0 = []
                allnotes1 = []
                allnotes2 = []
                allnotes3 = []
                allnotes4 = []
                allnotes5 = []
                ptb1 = []
                ptb2 = []
                ptb3 = []
                ptb4 = []
                ptb5 = []
                medicine1 = []
                medicine2 = []
                medicine3 = []
                medicine4 = []
                medicine5 = []

                rangeformed = 0
                rangeformed2 = 0
                rangeformed3 = 0
                rangeformed4 = 0
                rangeformed5 = 0

                for i in medicine1:
                    rangeformed+=1
                for i in medicine2:
                    rangeformed2+=1
                for i in medicine3:
                    rangeformed3+=1
                for i in medicine4:
                    rangeformed4+=1
                for i in medicine5:
                    rangeformed5+=1


                session_id = selectsession[0]["session_id"]
                seedspeciesid = selectsession[0]["seedspecies_id"]
                selectmed = selectsession[0]["medicinesession"]
                selectmed = selectmed.split("'")
                itemsselectmed = []
                idkcounter = 0
                med = ""
                medtwo = ""
                itemswewillc = []
                wow = dict()
                wowtwo = dict()
                wowthree = dict()
                wowfour = dict()
                wowfive = dict()
                elsee = 0
                iff = 0

                for i in selectmed:
                    med = i
                    ye = dict(med = med)
                    itemsselectmed.append(ye)
                    for idk in medicine1:

                        ww = idk[idkcounter]

                        if med in wow.keys():
                            wow[med].append(ww)
                        else:
                            wow[med] = [ww]

                        itemswewillc.append(wow)
                    idkcounter+=1

                idkcounter = 0
                for i in selectmed:
                    med = i
                    for idk in medicine2:
                        ww = idk[idkcounter]
                        if med in wowtwo.keys():
                            wowtwo[med].append(ww)
                        else:
                            wowtwo[med] = [ww]

                    idkcounter+=1

                idkcounter = 0
                for i in selectmed:
                    med = i
                    for idk in medicine3:
                        ww = idk[idkcounter]
                        if med in wowthree.keys():
                            wowthree[med].append(ww)
                        else:
                            wowthree[med] = [ww]

                    idkcounter+=1
                idkcounter = 0
                for i in selectmed:
                    med = i
                    for idk in medicine4:
                        ww = idk[idkcounter]
                        if med in wowfour.keys():
                            wowfour[med].append(ww)
                        else:
                            wowfour[med] = [ww]

                    idkcounter+=1
                idkcounter = 0
                for i in selectmed:
                    med = i
                    for idk in medicine5:
                        ww = idk[idkcounter]
                        if med in wowfive.keys():
                            wowfive[med].append(ww)
                        else:
                            wowfive[med] = [ww]

                    idkcounter+=1

                seedspeciestable = db.execute("SELECT * FROM seedspecies WHERE seedspecies_id = :seedspecies_id", seedspecies_id = seedspeciesid)
                seedspeciesname = seedspeciestable[0]["seedspecies_name"]

                selectsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)


                section_id = selectsection[0]["section_id"]
                calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
                pluster = 0
                for i,row in zip(allnotes0, calendarid):

                    waan = calendarid[pluster]["calendar_id"]
                    db.execute("UPDATE calendar SET daynote = :i WHERE calendar_id = :waan", i = i, waan = waan)
                    pluster+=1

                section_noteshfb = selectsection[0]["note"]
                selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)
                counterr = 0

                itemscalendarbeforelongtoong = []

                for row in selectcalendar:
                    c_date = selectcalendar[counterr]["date"]
                    c_day = selectcalendar[counterr]["day"]
                    weekday = selectcalendar[counterr]["WDay"]
                    c_lm = selectcalendar[counterr]["litermellon"]
                    c_lpd = selectcalendar[counterr]["literperday"]
                    c_rone = selectcalendar[counterr]["ratio_ones"]
                    c_rhun = selectcalendar[counterr]["ratio_hundreth"]
                    c_r = selectcalendar[counterr]["ratio"]
                    daynote = selectcalendar[counterr]["daynote"]
                    if daynote == None:
                        daynote = ""

                    itemsrow = dict(c_date = c_date, c_day = c_day, c_lm = c_lm, c_lpd = c_lpd
                    ,c_rone = c_rone, c_rhun = c_rhun, c_r = c_r,  weekday = weekday, daynote = daynote)
                    itemscalendarbeforelongtoong.append(itemsrow)
                    counterr+=1

                section_id = selectsection[1]["section_id"]
                section_notefhfb = selectsection[1]["note"]
                calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
                plusrfm = 0
                for w in range(rangeformed):
                    mmm = dict()
                    for i in wow:
                        ez = wow.get(i)
                        ez = ez[w]
                        mmm[i] = ez

                    jason = json.dumps(mmm,ensure_ascii=False)
                    waan = calendarid[plusrfm]["calendar_id"]
                    db.execute("UPDATE calendar SET medicinecal = :jason WHERE calendar_id = :waan", jason = jason, waan = waan)
                    plusrfm +=1

                #####TRYING STUFF######
                trymedcal = db.execute("SELECT medicinecal FROM calendar WHERE section_id = :section_id", section_id = section_id)
                trycounter = 0
                for row in trymedcal:
                    newww= trymedcal[trycounter]["medicinecal"]

                pluster = 0
                for i,row,h in zip(allnotes1, calendarid, ptb1):
                    waan = calendarid[pluster]["calendar_id"]
                    pluster+=1
                    db.execute("UPDATE calendar SET daynote = :i, ratiomedptb = :h WHERE calendar_id = :waan", i = i, waan = waan, h = h)

                selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb,medicinecal, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)
                itemsdynamic = []
                itemsanotherdynamic = []

                counterr = 0
                itemsselectptb = []
                itemsselectptbshfb = []
                itemsselectptbfhsb = []
                itemsselectptbshsb = []
                itemsselectptbthsb = []


                firstday = selectcalendar[1]["day"]
                firstday = int(firstday)
                itemsrowptbfhfb = dict(firstday = firstday)
                itemsselectptb.append(itemsrowptbfhfb)


                for row in selectcalendar:
                    c_datefhfb = selectcalendar[counterr]["date"]
                    weekdayfhfb = selectcalendar[counterr]["WDay"]
                    c_dayfhfb = selectcalendar[counterr]["day"]
                    c_lmfhfb = selectcalendar[counterr]["litermellon"]
                    c_lpdfhfb = selectcalendar[counterr]["literperday"]
                    c_ronesfhfb = selectcalendar[counterr]["ratio_ones"]
                    c_rhunfhfb = selectcalendar[counterr]["ratio_hundreth"]
                    c_rfhfb = selectcalendar[counterr]["ratio"]
                    daynotefhfb = selectcalendar[counterr]["daynote"]
                    medicinecalcalo = selectcalendar[counterr]["medicinecal"]
                    if medicinecalcalo == None:
                        medicinecalcal = ""
                        dictjumpen = {"waan":1 }
                        medicinecalcal = dictjumpen
                    else:
                        medicinecalcal = json.loads(medicinecalcalo)
                    if daynotefhfb == None:
                        daynotefhfb = ""
                    ptbfhfb = selectcalendar[counterr]["ratiomedptb"]
                    if ptbfhfb == None:
                        ptbfhfb = ""

                    itemsrowfhfb = dict(c_datefhfb = c_datefhfb, c_dayfhfb = c_dayfhfb, c_lmfhfb = c_lmfhfb, c_lpdfhfb = c_lpdfhfb
                    ,c_ronesfhfb = c_ronesfhfb, c_rhunfhfb = c_rhunfhfb, c_rfhfb = c_rfhfb, weekdayfhfb = weekdayfhfb, daynotefhfb = daynotefhfb, ptbfhfb = ptbfhfb,
                    medicinecalcal = medicinecalcal)

                    itemscalendarfhfb.append(itemsrowfhfb)
                    counterr+=1


                section_id = selectsection[2]["section_id"]
                calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
                plusrfm = 0
                for w in range(rangeformed2):
                    mmm = dict()
                    for i in wowtwo:
                        ez = wowtwo.get(i)
                        ez = ez[w]
                        mmm[i] = ez

                    jason = json.dumps(mmm,ensure_ascii=False)
                    waan = calendarid[plusrfm]["calendar_id"]
                    db.execute("UPDATE calendar SET medicinecal = :jason WHERE calendar_id = :waan", jason = jason, waan = waan)
                    plusrfm +=1

                pluster = 0
                for i,row,h in zip(allnotes2, calendarid, ptb2):
                    waan = calendarid[pluster]["calendar_id"]
                    pluster+=1
                    db.execute("UPDATE calendar SET daynote = :i, ratiomedptb = :h WHERE calendar_id = :waan", i = i, waan = waan, h = h)
                section_noteshfb = selectsection[2]["note"]
                selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb,medicinecal, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)
                counterr = 0




                for row in selectcalendar:
                    c_dateshfb = selectcalendar[counterr]["date"]
                    c_dayshfb = selectcalendar[counterr]["day"]
                    weekdayshfb = selectcalendar[counterr]["WDay"]
                    c_lmshfb = selectcalendar[counterr]["litermellon"]
                    c_lpdshfb = selectcalendar[counterr]["literperday"]
                    c_ronesshfb = selectcalendar[counterr]["ratio_ones"]
                    c_rhunshfb = selectcalendar[counterr]["ratio_hundreth"]
                    c_rshfb = selectcalendar[counterr]["ratio"]
                    daynoteshfb = selectcalendar[counterr]["daynote"]
                    medicinecalcaloshfb = selectcalendar[counterr]["medicinecal"]
                    if medicinecalcaloshfb == None:
                        medicinecalcalshfb = ""
                        dictjumpen = {"waan":1 }
                        medicinecalcalshfb = dictjumpen
                    else:
                        medicinecalcalshfb = json.loads(medicinecalcaloshfb)
                    if daynoteshfb == None:
                        daynoteshfb = ""
                    ptbshfb = selectcalendar[counterr]["ratiomedptb"]
                    if ptbshfb == None:
                        ptbshfb = ""
                    itemsrowshfb = dict(c_dateshfb = c_dateshfb, c_dayshfb = c_dayshfb, c_lmshfb = c_lmshfb, c_lpdshfb = c_lpdshfb
                    ,c_ronesshfb = c_ronesshfb, c_rhunshfb = c_rhunshfb, c_rshfb = c_rshfb,weekdayshfb = weekdayshfb, daynoteshfb = daynoteshfb, ptbshfb = ptbshfb
                    ,medicinecalcalshfb = medicinecalcalshfb)
                    itemscalendarshfb.append(itemsrowshfb)
                    counterr+=1





                section_id = selectsection[3]["section_id"]
                calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
                plusrfm = 0
                for w in range(rangeformed3):
                    mmm = dict()
                    for i in wowthree:
                        ez = wowthree.get(i)
                        ez = ez[w]
                        mmm[i] = ez

                    jason = json.dumps(mmm,ensure_ascii=False)
                    waan = calendarid[plusrfm]["calendar_id"]
                    db.execute("UPDATE calendar SET medicinecal = :jason WHERE calendar_id = :waan", jason = jason, waan = waan)
                    plusrfm +=1
                pluster = 0
                for i,row,h in zip(allnotes3, calendarid, ptb3):
                    waan = calendarid[pluster]["calendar_id"]
                    pluster+=1
                    db.execute("UPDATE calendar SET daynote = :i,ratiomedptb = :h WHERE calendar_id = :waan", i = i, waan = waan, h = h)
                section_notefhsb = selectsection[3]["note"]
                selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb,medicinecal, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)


                counterr = 0
                for row in selectcalendar:
                    c_datefhsb = selectcalendar[counterr]["date"]
                    c_dayfhsb = selectcalendar[counterr]["day"]
                    weekdayfhsb = selectcalendar[counterr]["WDay"]
                    c_lmfhsb = selectcalendar[counterr]["litermellon"]
                    c_lpdfhsb = selectcalendar[counterr]["literperday"]
                    c_ronesfhsb = selectcalendar[counterr]["ratio_ones"]
                    c_rhunfhsb = selectcalendar[counterr]["ratio_hundreth"]
                    c_rfhsb = selectcalendar[counterr]["ratio"]
                    daynotefhsb = selectcalendar[counterr]["daynote"]
                    medicinecalcalofhsb = selectcalendar[counterr]["medicinecal"]
                    if medicinecalcalofhsb == None:
                        medicinecalcalfhsb = ""
                        dictjumpen = {"waan":1 }
                        medicinecalcalfhsb = dictjumpen
                    else:
                        medicinecalcalfhsb = json.loads(medicinecalcalofhsb)
                    if daynotefhsb == None:
                        daynotefhsb = ""
                    ptbfhsb = selectcalendar[counterr]["ratiomedptb"]
                    if ptbfhsb == None:
                        ptbfhsb = ""
                    itemsrowfhsb = dict(c_datefhsb = c_datefhsb, c_dayfhsb = c_dayfhsb, c_lmfhsb = c_lmfhsb, c_lpdfhsb = c_lpdfhsb
                    ,c_ronesfhsb = c_ronesfhsb, c_rhunfhsb = c_rhunfhsb, c_rfhsb = c_rfhsb, weekdayfhsb = weekdayfhsb, daynotefhsb = daynotefhsb, ptbfhsb = ptbfhsb
                    ,medicinecalcalfhsb = medicinecalcalfhsb)
                    itemscalendarfhsb.append(itemsrowfhsb)
                    counterr+=1

                firstday = selectcalendar[0]["day"]
                firstday = int(firstday)

                itemsrowptbfhsb = dict(firstday = firstday)
                itemsselectptbfhsb.append(itemsrowptbfhsb)



                coun = 0
                section_id = selectsection[4]["section_id"]
                calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
                plusrfm = 0
                for w in range(rangeformed4):
                    mmm = dict()
                    for i in wowfour:
                        ez = wowfour.get(i)
                        ez = ez[w]
                        mmm[i] = ez


                    jason = json.dumps(mmm,ensure_ascii=False)
                    waan = calendarid[plusrfm]["calendar_id"]
                    db.execute("UPDATE calendar SET medicinecal = :jason WHERE calendar_id = :waan", jason = jason, waan = waan)
                    plusrfm +=1
                pluster = 0
                for i,row,h in zip(allnotes4, calendarid, ptb4):
                    waan = calendarid[pluster]["calendar_id"]
                    pluster+=1
                    db.execute("UPDATE calendar SET daynote = :i, ratiomedptb = :h WHERE calendar_id = :waan", i = i, waan = waan, h = h)

                section_noteshsb = selectsection[4]["note"]
                selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb,medicinecal, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)

                counterr = 0
                for row in selectcalendar:
                    c_dateshsb = selectcalendar[counterr]["date"]
                    c_dayshsb = selectcalendar[counterr]["day"]
                    weekdayshsb = selectcalendar[counterr]["WDay"]
                    c_lmshsb = selectcalendar[counterr]["litermellon"]
                    c_lpdshsb = selectcalendar[counterr]["literperday"]
                    c_ronesshsb = selectcalendar[counterr]["ratio_ones"]
                    c_rhunshsb = selectcalendar[counterr]["ratio_hundreth"]
                    c_rshsb = selectcalendar[counterr]["ratio"]
                    daynoteshsb = selectcalendar[counterr]["daynote"]
                    medicinecalcaloshsb = selectcalendar[counterr]["medicinecal"]
                    if medicinecalcaloshsb == None:
                        medicinecalcalshsb = ""
                        dictjumpen = {"waan":1 }
                        medicinecalcalshsb = dictjumpen
                    else:
                        medicinecalcalshsb = json.loads(medicinecalcaloshsb)
                    if daynoteshsb == None:
                        daynoteshsb = ""
                    ptbshsb = selectcalendar[counterr]["ratiomedptb"]
                    if ptbshsb == None:
                        ptbshsb = ""
                    itemsrowshsb = dict(c_dateshsb = c_dateshsb, c_dayshsb = c_dayshsb, c_lmshsb = c_lmshsb, c_lpdshsb = c_lpdshsb
                    ,c_ronesshsb = c_ronesshsb, c_rhunshsb = c_rhunshsb, c_rshsb = c_rshsb, weekdayshsb = weekdayshsb, daynoteshsb = daynoteshsb, ptbshsb = ptbshsb,
                    medicinecalcalshsb = medicinecalcalshsb)
                    itemscalendarshsb.append(itemsrowshsb)
                    counterr+=1

                firstday = selectcalendar[0]["day"]
                firstday = int(firstday)

                itemsrowptbshsb = dict(firstday = firstday)
                itemsselectptbshsb.append(itemsrowptbshsb)




                coun = 0
                section_id = selectsection[5]["section_id"]
                calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
                plusrfm = 0
                for w in range(rangeformed5):
                    mmm = dict()
                    for i in wowfive:
                        ez = wowfive.get(i)
                        ez = ez[w]
                        mmm[i] = ez

                    jason = json.dumps(mmm,ensure_ascii=False)
                    waan = calendarid[plusrfm]["calendar_id"]
                    db.execute("UPDATE calendar SET medicinecal = :jason WHERE calendar_id = :waan", jason = jason, waan = waan)
                    plusrfm +=1
                pluster = 0
                for i,row,h in zip(allnotes5, calendarid, ptb5):
                    waan = calendarid[pluster]["calendar_id"]
                    pluster+=1
                    db.execute("UPDATE calendar SET daynote = :i, ratiomedptb = :h WHERE calendar_id = :waan", i = i, waan = waan, h = h)

                section_notethsb = selectsection[5]["note"]
                selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb,medicinecal, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)

                counterr = 0
                for row in selectcalendar:
                    c_datethsb = selectcalendar[counterr]["date"]
                    c_daythsb = selectcalendar[counterr]["day"]
                    weekdaythsb = selectcalendar[counterr]["WDay"]
                    c_lmthsb = selectcalendar[counterr]["litermellon"]
                    c_lpdthsb = selectcalendar[counterr]["literperday"]
                    c_ronesthsb = selectcalendar[counterr]["ratio_ones"]
                    c_rhunthsb = selectcalendar[counterr]["ratio_hundreth"]
                    c_rthsb = selectcalendar[counterr]["ratio"]
                    daynotethsb = selectcalendar[counterr]["daynote"]
                    medicinecalcalothsb = selectcalendar[counterr]["medicinecal"]
                    if medicinecalcalothsb == None:
                        medicinecalcalthsb = ""
                        dictjumpen = {"waan":1 }
                        medicinecalcalthsb = dictjumpen
                    else:
                        medicinecalcalthsb = json.loads(medicinecalcalothsb)
                    if daynotethsb == None:
                        daynotethsb = ""
                    ptbthsb = selectcalendar[counterr]["ratiomedptb"]
                    if ptbthsb == None:
                        ptbthsb = ""
                    itemsrowthsb = dict(c_datethsb = c_datethsb, c_daythsb = c_daythsb, c_lmthsb = c_lmthsb, c_lpdthsb = c_lpdthsb
                    ,c_ronesthsb = c_ronesthsb, c_rhunthsb = c_rhunthsb, c_rthsb = c_rthsb, weekdaythsb = weekdaythsb, daynotethsb = daynotethsb, ptbthsb = ptbthsb,
                    medicinecalcalthsb = medicinecalcalthsb)
                    itemscalendarthsb.append(itemsrowthsb)
                    counterr+=1

                firstday = selectcalendar[0]["day"]
                firstday = int(firstday)

                itemsrowptbthsb = dict(firstday = firstday)
                itemsselectptbthsb.append(itemsrowptbthsb)
                return render_template("history.html", sessionname = sessionname,itemscalendarfhfb = itemscalendarfhfb, itemscalendarshfb = itemscalendarshfb, itemscalendarfhsb = itemscalendarfhsb, itemscalendarshsb = itemscalendarshsb, itemscalendarthsb = itemscalendarthsb, itemssection = itemssection
                ,seedspeciesname = seedspeciesname, section_notefhfb = section_notefhfb, section_noteshfb = section_noteshfb, section_notefhsb = section_notefhsb,
                section_noteshsb = section_noteshsb, section_notethsb = section_notethsb, itemsselectptb = itemsselectptb,itemsselectptbshfb = itemsselectptbshfb,itemsselectptbfhsb = itemsselectptbfhsb,
                itemsselectptbshsb = itemsselectptbshsb, itemsselectptbthsb = itemsselectptbthsb, capacityrong = capacityrong, rongname = rongname, itemsselectallptb = itemsselectallptb, itemsselectmed = itemsselectmed, itemsdynamic = itemsdynamic, itemsanotherdynamic = itemsanotherdynamic,
                itemscalendarbeforelongtoong = itemscalendarbeforelongtoong)






    return render_template("historyselect.html", itemssessionnum = itemssessionnum)

@app.route("/history", methods=["GET", "POST"])
def history():
#select history
    rong_id = session["rongg_id"]
    rongname = session["rongg_name"]
    sessionnamee = session["sessionname"]

    rongg = db.execute("SELECT * FROM rong WHERE rong_id = :rong_id", rong_id = rong_id)


    return render_template("history.html", sessionnamee = sessionnamee)

@app.route("/currenttable", methods=["GET", "POST"])
def currenttable():

    rong_id = session["rongg_id"]
    rongname = session["rongg_name"]
    itemscalendarfhfb = []
    itemscalendarshfb = []
    itemscalendarfhsb = []
    itemscalendarshsb = []
    itemscalendarthsb = []
    itemssection = []
    itemsselectallptb = [None]


    rongg = db.execute("SELECT * FROM rong WHERE rong_id = :rong_id", rong_id = rong_id)
    allptb = db.execute("SELECT * FROM ptb WHERE booleanptb = 1")
    ounter = 0

    for row in allptb:
        ptball = allptb[ounter]["ratiomed"]
        itemsallptb = dict(ptball = ptball)
        itemsselectallptb.append(itemsallptb)
        ounter +=1

    capacityrong = rongg[0]["rong_capacity"]
    rongname = rongg[0]["rong_name"]
    selectsession = db.execute("SELECT MAX(session_id) AS session_id, seedspecies_id,medicinesession FROM session WHERE rong_id = :rong_id", rong_id = rong_id)
    session_id = selectsession[0]["session_id"]
    allcalendar = db.execute("SELECT * FROM calendar JOIN section ON section.section_id = calendar.section_id JOIN session ON session.session_id = section.session_id WHERE session.session_id = :selectsession", selectsession = session_id)

    allnotes0 = []
    allnotes1 = []
    allnotes2 = []
    allnotes3 = []
    allnotes4 = []
    allnotes5 = []
    ptb1 = []
    ptb2 = []
    ptb3 = []
    ptb4 = []
    ptb5 = []
    medicine1 = []
    medicine2 = []
    medicine3 = []
    medicine4 = []
    medicine5 = []
    itemscapacity = []

#get variable that was already save update it and select it
    if request.content_type == "application/json":
        allnotes0 = request.json['itemsallnotes0']
        allnotes1 = request.json['itemsallnotes1']
        allnotes2 = request.json['itemsallnotes2']
        allnotes3 = request.json['itemsallnotes3']
        allnotes4 = request.json['itemsallnotes4']
        allnotes5 = request.json['itemsallnotes5']
        ptb1 = request.json['itemsptb1']
        ptb2 = request.json['itemsptb2']
        ptb3 = request.json['itemsptb3']
        ptb4 = request.json['itemsptb4']
        ptb5 = request.json['itemsptb5']
        medicine1 = request.json['itemsmedicinenew']
        medicine2 = request.json['itemsmedicinenew2']
        medicine3 = request.json['itemsmedicinenew3']
        medicine4 = request.json['itemsmedicinenew4']
        medicine5 = request.json['itemsmedicinenew5']
        itemscapacity = request.json['itemscapacity']


    rangeformed = 0
    rangeformed2 = 0
    rangeformed3 = 0
    rangeformed4 = 0
    rangeformed5 = 0



    for i in medicine1:
        rangeformed+=1
    for i in medicine2:
        rangeformed2+=1
    for i in medicine3:
        rangeformed3+=1
    for i in medicine4:
        rangeformed4+=1
    for i in medicine5:
        rangeformed5+=1
    plus = 0
    for i in itemscapacity:
        capacity = allcalendar[plus]["capacity"]
        calendar_id = allcalendar[plus]["calendar_id"]
        db.execute("UPDATE calendar SET capacity = :i WHERE calendar_id = :calendar_id", i = i, calendar_id = calendar_id)
        plus+=1



    session_id = selectsession[0]["session_id"]
    seedspeciesid = selectsession[0]["seedspecies_id"]
    selectmed = selectsession[0]["medicinesession"]
    selectmed = selectmed.split("'")

    itemsselectmed = []
    idkcounter = 0
    med = ""
    medtwo = ""
    itemswewillc = []
    wow = dict()
    wowtwo = dict()
    wowthree = dict()
    wowfour = dict()
    wowfive = dict()
    elsee = 0
    iff = 0

    for i in selectmed:
        med = i

        ye = dict(med = med)
        itemsselectmed.append(ye)
        for idk in medicine1:


            ww = idk[idkcounter]

            if med in wow.keys():
                wow[med].append(ww)
            else:
                wow[med] = [ww]

            itemswewillc.append(wow)
        idkcounter+=1

    idkcounter = 0
    for i in selectmed:
        med = i
        for idk in medicine2:
            ww = idk[idkcounter]
            if med in wowtwo.keys():
                wowtwo[med].append(ww)
            else:
                wowtwo[med] = [ww]

        idkcounter+=1

    idkcounter = 0
    for i in selectmed:
        med = i
        for idk in medicine3:
            ww = idk[idkcounter]
            if med in wowthree.keys():
                wowthree[med].append(ww)
            else:
                wowthree[med] = [ww]

        idkcounter+=1
    idkcounter = 0
    for i in selectmed:
        med = i
        for idk in medicine4:
            ww = idk[idkcounter]
            if med in wowfour.keys():
                wowfour[med].append(ww)
            else:
                wowfour[med] = [ww]

        idkcounter+=1
    idkcounter = 0
    for i in selectmed:
        med = i
        for idk in medicine5:
            ww = idk[idkcounter]
            if med in wowfive.keys():
                wowfive[med].append(ww)
            else:
                wowfive[med] = [ww]

        idkcounter+=1



    seedspeciestable = db.execute("SELECT * FROM seedspecies WHERE seedspecies_id = :seedspecies_id", seedspecies_id = seedspeciesid)
    seedspeciesname = seedspeciestable[0]["seedspecies_name"]

    selectsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)


    section_id = selectsection[0]["section_id"]
    calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
    pluster = 0
    for i,row in zip(allnotes0, calendarid):

        waan = calendarid[pluster]["calendar_id"]

        db.execute("UPDATE calendar SET daynote = :i WHERE calendar_id = :waan", i = i, waan = waan)
        pluster+=1

    section_noteshfb = selectsection[0]["note"]
    selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb,eccalendar, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)
    counterr = 0

    itemscalendarbeforelongtoong = []

    for row in selectcalendar:
        c_date = selectcalendar[counterr]["date"]
        c_day = selectcalendar[counterr]["day"]
        weekday = selectcalendar[counterr]["WDay"]
        c_lm = selectcalendar[counterr]["litermellon"]
        c_lpd = selectcalendar[counterr]["literperday"]
        c_rone = selectcalendar[counterr]["ratio_ones"]
        c_rhun = selectcalendar[counterr]["ratio_hundreth"]
        c_r = selectcalendar[counterr]["ratio"]
        daynote = selectcalendar[counterr]["daynote"]
        eccalendar = selectcalendar[counterr]["eccalendar"]
        eccalendar = float(eccalendar)
        c_lm = float(c_lm)

        if daynote == None:
            daynote = ""

        itemsrow = dict(c_date = c_date, c_day = c_day, c_lm = c_lm, c_lpd = c_lpd
        ,c_rone = c_rone, c_rhun = c_rhun, c_r = c_r, weekday = weekday, daynote = daynote, eccalendar = eccalendar)
        itemscalendarbeforelongtoong.append(itemsrow)
        counterr+=1



    section_id = selectsection[1]["section_id"]
    section_notefhfb = selectsection[1]["note"]
    calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
    plusrfm = 0
    for w in range(rangeformed):
        mmm = dict()
        for i in wow:
            ez = wow.get(i)
            ez = ez[w]
            mmm[i] = ez

        jason = json.dumps(mmm,ensure_ascii=False)
        waan = calendarid[plusrfm]["calendar_id"]
        db.execute("UPDATE calendar SET medicinecal = :jason WHERE calendar_id = :waan", jason = jason, waan = waan)
        plusrfm +=1

    #####TRYING STUFF######
    trymedcal = db.execute("SELECT medicinecal FROM calendar WHERE section_id = :section_id", section_id = section_id)
    trycounter = 0
    for row in trymedcal:
        trymedcal[trycounter]["medicinecal"]


    pluster = 0
    for i,row,h in zip(allnotes1, calendarid, ptb1):
        waan = calendarid[pluster]["calendar_id"]
        pluster+=1
        db.execute("UPDATE calendar SET daynote = :i, ratiomedptb = :h WHERE calendar_id = :waan", i = i, waan = waan, h = h)


    selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb,medicinecal,capacity,eccalendar, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)
    itemsdynamic = []
    itemsanotherdynamic = []

    counterr = 0
    itemsselectptb = []
    itemsselectptbshfb = []
    itemsselectptbfhsb = []
    itemsselectptbshsb = []
    itemsselectptbthsb = []


    firstday = selectcalendar[1]["day"]
    firstday = int(firstday)

    itemsrowptbfhfb = dict(firstday = firstday)
    itemsselectptb.append(itemsrowptbfhfb)




    for row in selectcalendar:
        c_datefhfb = selectcalendar[counterr]["date"]
        weekdayfhfb = selectcalendar[counterr]["WDay"]
        c_dayfhfb = selectcalendar[counterr]["day"]
        c_lmfhfb = selectcalendar[counterr]["litermellon"]
        c_lpdfhfb = selectcalendar[counterr]["literperday"]
        c_ronesfhfb = selectcalendar[counterr]["ratio_ones"]
        c_rhunfhfb = selectcalendar[counterr]["ratio_hundreth"]
        c_rfhfb = selectcalendar[counterr]["ratio"]
        daynotefhfb = selectcalendar[counterr]["daynote"]
        medicinecalcalo = selectcalendar[counterr]["medicinecal"]
        capacityfhfb = selectcalendar[counterr]["capacity"]
        eccalendarfhfb = selectcalendar[counterr]["eccalendar"]
        eccalendarfhfb = float(eccalendarfhfb)
        c_lmfhfb = float(c_lmfhfb)
        if capacityfhfb == None:
            capacityfhfb = ""

        if medicinecalcalo == None:
            medicinecalcal = ""
            dictjumpen = {"waan":1 }
            medicinecalcal = dictjumpen
        else:
            medicinecalcal = json.loads(medicinecalcalo)

        if daynotefhfb == None:
            daynotefhfb = ""
        ptbfhfb = selectcalendar[counterr]["ratiomedptb"]
        if ptbfhfb == None:
            ptbfhfb = ""

        itemsrowfhfb = dict(c_datefhfb = c_datefhfb, c_dayfhfb = c_dayfhfb, c_lmfhfb = c_lmfhfb, c_lpdfhfb = c_lpdfhfb
        ,c_ronesfhfb = c_ronesfhfb, c_rhunfhfb = c_rhunfhfb, c_rfhfb = c_rfhfb, weekdayfhfb = weekdayfhfb, daynotefhfb = daynotefhfb, ptbfhfb = ptbfhfb,
        medicinecalcal = medicinecalcal, capacityfhfb = capacityfhfb, eccalendarfhfb = eccalendarfhfb)

        itemscalendarfhfb.append(itemsrowfhfb)
        counterr+=1


    section_id = selectsection[2]["section_id"]
    calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
    plusrfm = 0
    for w in range(rangeformed2):
        mmm = dict()
        for i in wowtwo:
            ez = wowtwo.get(i)
            ez = ez[w]
            mmm[i] = ez

        jason = json.dumps(mmm,ensure_ascii=False)
        waan = calendarid[plusrfm]["calendar_id"]
        db.execute("UPDATE calendar SET medicinecal = :jason WHERE calendar_id = :waan", jason = jason, waan = waan)
        plusrfm +=1

    pluster = 0
    for i,row,h in zip(allnotes2, calendarid, ptb2):
        waan = calendarid[pluster]["calendar_id"]
        pluster+=1
        db.execute("UPDATE calendar SET daynote = :i, ratiomedptb = :h WHERE calendar_id = :waan", i = i, waan = waan, h = h)
    section_noteshfb = selectsection[2]["note"]
    selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb,medicinecal,capacity,eccalendar, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)
    counterr = 0




    for row in selectcalendar:
        c_dateshfb = selectcalendar[counterr]["date"]
        c_dayshfb = selectcalendar[counterr]["day"]
        if c_dayshfb == "30" or c_dayshfb == "31" or c_dayshfb ==  "32" or c_dayshfb == "33" or c_dayshfb == "34" or c_dayshfb == "35":
            pasom = c_dayshfb
            print(f"this is pasom: {pasom}")
        else:
            pasom = "false"
        weekdayshfb = selectcalendar[counterr]["WDay"]
        c_lmshfb = selectcalendar[counterr]["litermellon"]
        c_lpdshfb = selectcalendar[counterr]["literperday"]
        c_ronesshfb = selectcalendar[counterr]["ratio_ones"]
        c_rhunshfb = selectcalendar[counterr]["ratio_hundreth"]
        c_rshfb = selectcalendar[counterr]["ratio"]
        daynoteshfb = selectcalendar[counterr]["daynote"]
        medicinecalcaloshfb = selectcalendar[counterr]["medicinecal"]
        capacityshfb = selectcalendar[counterr]["capacity"]
        eccalendarshfb = selectcalendar[counterr]["eccalendar"]
        eccalendarshfb = float(eccalendarshfb)
        c_lmshfb = float(c_lmshfb)
        if capacityshfb == None:
            capacityshfb = ""
        if medicinecalcaloshfb == None:
            medicinecalcalshfb = ""
            dictjumpen = {"waan":1 }
            medicinecalcalshfb = dictjumpen
        else:
            medicinecalcalshfb = json.loads(medicinecalcaloshfb)
        if daynoteshfb == None:
            daynoteshfb = ""
        ptbshfb = selectcalendar[counterr]["ratiomedptb"]
        if ptbshfb == None:
            ptbshfb = ""
        itemsrowshfb = dict(c_dateshfb = c_dateshfb, c_dayshfb = c_dayshfb, c_lmshfb = c_lmshfb, c_lpdshfb = c_lpdshfb
        ,c_ronesshfb = c_ronesshfb, c_rhunshfb = c_rhunshfb, c_rshfb = c_rshfb, weekdayshfb = weekdayshfb, daynoteshfb = daynoteshfb, ptbshfb = ptbshfb
        ,medicinecalcalshfb = medicinecalcalshfb, capacityshfb = capacityshfb, eccalendarshfb = eccalendarshfb, pasom = pasom)
        itemscalendarshfb.append(itemsrowshfb)
        counterr+=1





    section_id = selectsection[3]["section_id"]
    calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
    plusrfm = 0
    for w in range(rangeformed3):
        mmm = dict()
        cunter = 0
        cunter2 = 0
        for i in wowthree:
            ez = wowthree.get(i)
            ez = ez[w]
            mmm[i] = ez

            if ez == "":
                cunter2 += 1
            cunter+=1
        print(f"cunter:{cunter}")
        print(f"cunter2: {cunter2}")


        jason = json.dumps(mmm,ensure_ascii=False)
        waan = calendarid[plusrfm]["calendar_id"]
        db.execute("UPDATE calendar SET medicinecal = :jason WHERE calendar_id = :waan", jason = jason, waan = waan)
        plusrfm +=1
    pluster = 0
    for i,row,h in zip(allnotes3, calendarid, ptb3):
        waan = calendarid[pluster]["calendar_id"]
        pluster+=1
        db.execute("UPDATE calendar SET daynote = :i,ratiomedptb = :h WHERE calendar_id = :waan", i = i, waan = waan, h = h)
    section_notefhsb = selectsection[3]["note"]
    selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb,medicinecal,capacity,eccalendar, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)


    counterr = 0
    for row in selectcalendar:

        c_datefhsb = selectcalendar[counterr]["date"]
        c_dayfhsb = selectcalendar[counterr]["day"]
        if c_dayfhsb == "30" or c_dayfhsb == "31" or c_dayfhsb ==  "32" or c_dayfhsb == "33" or c_dayfhsb == "34" or c_dayfhsb == "35":
            pasom = c_dayfhsb
            print(f"this is pasom: {pasom}")
        else:
            pasom = "false"
        weekdayfhsb = selectcalendar[counterr]["WDay"]
        c_lmfhsb = selectcalendar[counterr]["litermellon"]
        c_lpdfhsb = selectcalendar[counterr]["literperday"]
        c_ronesfhsb = selectcalendar[counterr]["ratio_ones"]
        c_rhunfhsb = selectcalendar[counterr]["ratio_hundreth"]
        c_rfhsb = selectcalendar[counterr]["ratio"]
        daynotefhsb = selectcalendar[counterr]["daynote"]
        medicinecalcalofhsb = selectcalendar[counterr]["medicinecal"]
        capacityfhsb = selectcalendar[counterr]["capacity"]
        eccalendarfhsb = selectcalendar[counterr]["eccalendar"]
        eccalendarfhsb = float(eccalendarfhsb)
        c_lmfhsb = float(c_lmfhsb)
        if capacityfhsb == None:
            capacityfhsb = ""
        if medicinecalcalofhsb == None:
            medicinecalcalfhsb = ""
            dictjumpen = {"waan":1 }
            medicinecalcalfhsb = dictjumpen
        else:
            medicinecalcalfhsb = json.loads(medicinecalcalofhsb)
        if daynotefhsb == None:
            daynotefhsb = ""
        ptbfhsb = selectcalendar[counterr]["ratiomedptb"]
        if ptbfhsb == None:
            ptbfhsb = ""
        itemsrowfhsb = dict(c_datefhsb = c_datefhsb, c_dayfhsb = c_dayfhsb, c_lmfhsb = c_lmfhsb, c_lpdfhsb = c_lpdfhsb
        ,c_ronesfhsb = c_ronesfhsb, c_rhunfhsb = c_rhunfhsb, c_rfhsb = c_rfhsb, weekdayfhsb = weekdayfhsb, daynotefhsb = daynotefhsb, ptbfhsb = ptbfhsb
        ,medicinecalcalfhsb = medicinecalcalfhsb, capacityfhsb = capacityfhsb, eccalendarfhsb = eccalendarfhsb, pasom = pasom)
        itemscalendarfhsb.append(itemsrowfhsb)
        counterr+=1

    firstday = selectcalendar[0]["day"]
    firstday = int(firstday)

    itemsrowptbfhsb = dict(firstday = firstday)
    itemsselectptbfhsb.append(itemsrowptbfhsb)



    coun = 0
    section_id = selectsection[4]["section_id"]
    calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
    plusrfm = 0
    for w in range(rangeformed4):
        mmm = dict()
        cunter = 0
        cunter2 = 0
        for i in wowfour:
            ez = wowfour.get(i)
            ez = ez[w]
            mmm[i] = ez
            if ez == "":
                cunter2 += 1
                cunter+=1
        print(f"cunter:{cunter}")
        print(f"cunter2: {cunter2}")

        jason = json.dumps(mmm,ensure_ascii=False)
        waan = calendarid[plusrfm]["calendar_id"]
        db.execute("UPDATE calendar SET medicinecal = :jason WHERE calendar_id = :waan", jason = jason, waan = waan)
        plusrfm +=1
    pluster = 0
    for i,row,h in zip(allnotes4, calendarid, ptb4):
        waan = calendarid[pluster]["calendar_id"]
        pluster+=1
        db.execute("UPDATE calendar SET daynote = :i, ratiomedptb = :h WHERE calendar_id = :waan", i = i, waan = waan, h = h)

    section_noteshsb = selectsection[4]["note"]
    selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb,medicinecal,capacity,eccalendar, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)

    counterr = 0
    for row in selectcalendar:

        c_dateshsb = selectcalendar[counterr]["date"]
        c_dayshsb = selectcalendar[counterr]["day"]
        weekdayshsb = selectcalendar[counterr]["WDay"]
        c_lmshsb = selectcalendar[counterr]["litermellon"]
        c_lpdshsb = selectcalendar[counterr]["literperday"]
        c_ronesshsb = selectcalendar[counterr]["ratio_ones"]
        c_rhunshsb = selectcalendar[counterr]["ratio_hundreth"]
        c_rshsb = selectcalendar[counterr]["ratio"]
        daynoteshsb = selectcalendar[counterr]["daynote"]
        medicinecalcaloshsb = selectcalendar[counterr]["medicinecal"]
        capacityshsb = selectcalendar[counterr]["capacity"]
        eccalendarshsb = selectcalendar[counterr]["eccalendar"]
        eccalendarshsb = float(eccalendarshsb)
        c_lmshsb = float(c_lmshsb)
        if capacityshsb == None:
            capacityshsb = ""
        if medicinecalcaloshsb == None:
            medicinecalcalshsb = ""
            dictjumpen = {"waan":1 }
            medicinecalcalshsb = dictjumpen
        else:
            medicinecalcalshsb = json.loads(medicinecalcaloshsb)
        if daynoteshsb == None:
            daynoteshsb = ""
        ptbshsb = selectcalendar[counterr]["ratiomedptb"]
        if ptbshsb == None:
            ptbshsb = ""
        itemsrowshsb = dict(c_dateshsb = c_dateshsb, c_dayshsb = c_dayshsb, c_lmshsb = c_lmshsb, c_lpdshsb = c_lpdshsb
        ,c_ronesshsb = c_ronesshsb, c_rhunshsb = c_rhunshsb, c_rshsb = c_rshsb,weekdayshsb = weekdayshsb, daynoteshsb = daynoteshsb, ptbshsb = ptbshsb,
        medicinecalcalshsb = medicinecalcalshsb, capacityshsb = capacityshsb, eccalendarshsb = eccalendarshsb)
        itemscalendarshsb.append(itemsrowshsb)
        counterr+=1

    firstday = selectcalendar[0]["day"]
    firstday = int(firstday)

    itemsrowptbshsb = dict(firstday = firstday)
    itemsselectptbshsb.append(itemsrowptbshsb)




    coun = 0
    section_id = selectsection[5]["section_id"]
    calendarid = db.execute("SELECT calendar_id FROM calendar WHERE section_id = :section_id", section_id = section_id)
    plusrfm = 0
    for w in range(rangeformed5):
        mmm = dict()
        for i in wowfive:
            ez = wowfive.get(i)
            ez = ez[w]
            mmm[i] = ez

        jason = json.dumps(mmm,ensure_ascii=False)
        waan = calendarid[plusrfm]["calendar_id"]
        db.execute("UPDATE calendar SET medicinecal = :jason WHERE calendar_id = :waan", jason = jason, waan = waan)
        plusrfm +=1
    pluster = 0
    for i,row,h in zip(allnotes5, calendarid, ptb5):
        waan = calendarid[pluster]["calendar_id"]
        pluster+=1
        db.execute("UPDATE calendar SET daynote = :i, ratiomedptb = :h WHERE calendar_id = :waan", i = i, waan = waan, h = h)

    section_notethsb = selectsection[5]["note"]
    selectcalendar = db.execute("SELECT day,date,litermellon,literperday,ratio_ones,ratio_hundreth,ratio,daynote,ratiomedptb,medicinecal,capacity,eccalendar, CASE strftime('%w',date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END WDay FROM calendar WHERE section_id = :section_id ", section_id = section_id)

    if request.content_type == "application/json":
        if 'checkforsave' in request.json.keys():
            checkforsave = request.json['checkforsave']
            return ({'checkforsave':checkforsave} ,200, {'ContentType':'application/json'})




    counterr = 0
    for row in selectcalendar:
        c_datethsb = selectcalendar[counterr]["date"]
        c_daythsb = selectcalendar[counterr]["day"]
        weekdaythsb = selectcalendar[counterr]["WDay"]
        c_lmthsb = selectcalendar[counterr]["litermellon"]
        c_lpdthsb = selectcalendar[counterr]["literperday"]
        c_ronesthsb = selectcalendar[counterr]["ratio_ones"]
        c_rhunthsb = selectcalendar[counterr]["ratio_hundreth"]
        c_rthsb = selectcalendar[counterr]["ratio"]
        daynotethsb = selectcalendar[counterr]["daynote"]
        medicinecalcalothsb = selectcalendar[counterr]["medicinecal"]
        capacitythsb = selectcalendar[counterr]["capacity"]
        eccalendarthsb = selectcalendar[counterr]["eccalendar"]
        eccalendarthsb = float(eccalendarthsb)
        c_lmthsb = float(c_lmthsb)
        if capacitythsb == None:
            capacitythsb = ""
        if medicinecalcalothsb == None:
            medicinecalcalthsb = ""
            dictjumpen = {"waan":1 }
            medicinecalcalthsb = dictjumpen
        else:
            medicinecalcalthsb = json.loads(medicinecalcalothsb)
        if daynotethsb == None:
            daynotethsb = ""
        ptbthsb = selectcalendar[counterr]["ratiomedptb"]
        if ptbthsb == None:
            ptbthsb = ""
        itemsrowthsb = dict(c_datethsb = c_datethsb, c_daythsb = c_daythsb, c_lmthsb = c_lmthsb, c_lpdthsb = c_lpdthsb
        ,c_ronesthsb = c_ronesthsb, c_rhunthsb = c_rhunthsb, c_rthsb = c_rthsb, weekdaythsb = weekdaythsb, daynotethsb = daynotethsb, ptbthsb = ptbthsb,
        medicinecalcalthsb = medicinecalcalthsb, capacitythsb = capacitythsb, eccalendarthsb = eccalendarthsb)
        itemscalendarthsb.append(itemsrowthsb)
        counterr+=1

    firstday = selectcalendar[0]["day"]
    firstday = int(firstday)

    itemsrowptbthsb = dict(firstday = firstday)
    itemsselectptbthsb.append(itemsrowptbthsb)




    return render_template("currenttable.html", itemscalendarfhfb = itemscalendarfhfb, itemscalendarshfb = itemscalendarshfb, itemscalendarfhsb = itemscalendarfhsb, itemscalendarshsb = itemscalendarshsb, itemscalendarthsb = itemscalendarthsb, itemssection = itemssection
    ,seedspeciesname = seedspeciesname, section_notefhfb = section_notefhfb, section_noteshfb = section_noteshfb, section_notefhsb = section_notefhsb,
    section_noteshsb = section_noteshsb, section_notethsb = section_notethsb, itemsselectptb = itemsselectptb,itemsselectptbshfb = itemsselectptbshfb,itemsselectptbfhsb = itemsselectptbfhsb,
    itemsselectptbshsb = itemsselectptbshsb, itemsselectptbthsb = itemsselectptbthsb, capacityrong = capacityrong, rongname = rongname, itemsselectallptb = itemsselectallptb, itemsselectmed = itemsselectmed, itemsdynamic = itemsdynamic, itemsanotherdynamic = itemsanotherdynamic,
    itemscalendarbeforelongtoong = itemscalendarbeforelongtoong)

@app.route("/information", methods=["GET", "POST"])
def information():
    changeupdate = ""
    #based on the route users take to get here (new or change)
    print("information!!!")
    itemsddseedspecies = [None]
    itemsptbdd = []

    itemsmedicinedd = [None]
    itemsnothing = []
    itemsassumption = [None]
    itemsthassumption = []


    seedddspecies = db.execute("SELECT seedspecies_id, seedspecies_name FROM seedspecies WHERE booleanseedspecies = 1")
    assumptioninform = db.execute("SELECT assumptionkey, assumption_name FROM assumption")
    ptbdd = db.execute("SELECT ptb_id, ratiomed FROM ptb WHERE booleanptb = 1")
    medicinedd = db.execute("SELECT medicine_id, medicine_name FROM medicine WHERE booleanmedicine = 1")

    counter = 0
    rong_id = session["rongg_id"]
    rongname = session["rongg_name"]
    if request.method == "POST":

        changeupdate = ""


        if "changebutt" in request.form.keys():
            changeupdate = "true"

        if request.content_type == "application/json":
            if 'id' not in request.json.keys():

                changeupdate = request.json['changeupdate']
                fb = request.json['fb']
                seedspeciesid = request.json['seedspeciesname']
                assumption_val = request.json['assumption_val']
                itemsthassumption.append(assumption_val)
                selectmed = request.json['itemsselectmed']
                longtoongdays = request.json['longtoongdays']

                letstryrong = db.execute("SELECT * FROM rong WHERE rong_id = :rong_id", rong_id = rong_id)
                seedspeciesrealid = db.execute("SELECT * FROM seedspecies WHERE seedspecies_name = :seedspeciesid", seedspeciesid = seedspeciesid)
                seedspeciesrealid = seedspeciesrealid[0]["seedspecies_id"]
                rongcapacity = letstryrong[0]["rong_capacity"]
                sessionname = request.json['sessionname']

                if changeupdate == "true":
                    selectsession = db.execute("SELECT MAX(session_id) AS session_id, seedspecies_id,sessionname,medicinesession,beforelongtoong,assumption_val,firstblocknumdays FROM session WHERE rong_id = :rong_id", rong_id = rong_id)
                    session_id = selectsession[0]["session_id"]
                    sessionno = db.execute("UPDATE session SET seedspecies_id = :seedspeciesrealid, firstblocknumdays = :fb, rong_id = :rong_id, sessionname = :sessionname, medicinesession = :selectmed, beforelongtoong = :longtoongdays, assumption_val = :assumption_val WHERE session_id = :session_id", seedspeciesrealid = seedspeciesrealid, fb = fb, rong_id = rong_id, sessionname = sessionname,selectmed = selectmed ,longtoongdays = longtoongdays, assumption_val = assumption_val, session_id = session_id)

                else:
                    sessionstatus = 1
                    sessionno = db.execute("INSERT INTO session (seedspecies_id, firstblocknumdays, rong_id, sessionname,medicinesession, beforelongtoong, assumption_val, sessionstatus) VALUES(?,?,?,?,?,?,?,?)", seedspeciesrealid, fb, rong_id, sessionname,selectmed,longtoongdays, assumption_val, sessionstatus)

    #FHFB----------------------------------------------------------------------------------
                fhfb = request.json['fhfb']
                fhfb = int(fhfb)
                longtoongdays = int(longtoongdays)
                ratiofhfb = request.json['ratiofhfb']
                ratio1fhfb = "1:1"
                ratio2fhfb = "50:50"
                notefhfb = request.json['notefhfb']
                capacity_ones = 0.6
                capacity_hundreth = rongcapacity * capacity_ones
                capacity_hundreth = int(capacity_hundreth)

                if changeupdate == "true":
                   electsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)

                   section_id0 = electsection[0]["section_id"]
                   db.execute("UPDATE section SET note = '', sectionblock = 0 WHERE section_id = :section_id0",section_id0 = section_id0)
                else:
                    sectionno = db.execute("INSERT INTO section (session_id,note,sectionblock) VALUES(?,?,?)",sessionno, "", 0)



                startdate = request.json['startdate']
                startdate = datetime.strptime(startdate,"%Y-%m-%d").date()
                fhfb = int(fhfb)
                ptbcounter = 0
                ptbdayslist = []
                ptbidlist = []
                blongtoong = 0
                if changeupdate == "true":
                    electsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)
                    section_id = electsection[0]["section_id"]
                    db.execute("DELETE FROM calendar WHERE section_id = :section_id", section_id = section_id)
                    for i in range(longtoongdays):
                        beforelongtoong = startdate + timedelta(i)
                        blongtoong = i + 1
                        eccalendar = 0
                        # you can put ec in as 0 for before long toong days
                        db.execute("INSERT INTO calendar (section_id,date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)",section_id, beforelongtoong, 0, 0, "", "", "", blongtoong, eccalendar)

                else:
                    for i in range(longtoongdays):
                        beforelongtoong = startdate + timedelta(i)
                        blongtoong = i + 1
                        eccalendar = 0
                        db.execute("INSERT INTO calendar (section_id,date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)",sectionno, beforelongtoong, 0, 0, "", "", "", blongtoong, eccalendar)


                dateptbfhfb = startdate
                startdate = startdate + timedelta(longtoongdays)

                if changeupdate == "true":
                    electsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)
                    section_id1 = electsection[1]["section_id"]
                    db.execute("UPDATE section SET note = :notefhfb, sectionblock = :fhfb WHERE section_id = :section_id1", notefhfb = notefhfb, fhfb = fhfb, section_id1 = section_id1)
                else:
                    sectionno = db.execute("INSERT INTO section (session_id,note,sectionblock) VALUES(?,?,?)",sessionno, notefhfb, fhfb)

                dayfhfb = 0
                if changeupdate == "true":
                    db.execute("DELETE FROM calendar WHERE section_id = :section_id", section_id = section_id1)
                    for i in range(fhfb):
                        datefhfb = startdate + timedelta(i)
                        dayfhfb = blongtoong + i + 1
                        eccalendar = 1.0
                        literperday = 1.0
                        if dayfhfb > 20 and dayfhfb < 25:
                            eccalendar = 1.2
                            literperday = 1.0
                        if dayfhfb > 24 and dayfhfb < 29:
                            eccalendar = 1.8
                            literperday = 1.0
                        if dayfhfb > 28 and dayfhfb < 61:
                            eccalendar = 2.0
                            literperday = 1.6
                        if dayfhfb > 60:
                            eccalendar = 1.5
                            literperday = 1.2
                        db.execute("INSERT INTO calendar (section_id, date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)", section_id1, datefhfb, literperday, capacity_hundreth,ratio1fhfb, ratio2fhfb, ratiofhfb, dayfhfb, eccalendar)
                else:
                    for i in range(fhfb):
                        datefhfb = startdate + timedelta(i)
                        dayfhfb = blongtoong + i + 1
                        eccalendar = 1.0
                        literperday = 1.0
                        if dayfhfb > 20 and dayfhfb < 25:
                            eccalendar = 1.2
                            literperday = 1.0
                        if dayfhfb > 24 and dayfhfb < 29:
                            eccalendar = 1.8
                            literperday = 1.0
                        if dayfhfb > 28 and dayfhfb < 61:
                            eccalendar = 2.0
                            literperday = 1.6
                        if dayfhfb > 60:
                            eccalendar = 1.5
                            literperday = 1.2
                        db.execute("INSERT INTO calendar (section_id, date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)", sectionno, datefhfb, literperday, capacity_hundreth,ratio1fhfb, ratio2fhfb, ratiofhfb, dayfhfb, eccalendar)


    #SHFB-------------------------------------------------------------------------------------
                shfb = request.json['shfb']
                shfb = int(shfb)
                ratioshfb = request.json['ratioshfb']
                ratio1shfb = "1.25:1"
                ratio2shfb = "56:44"
                noteshfb = request.json['noteshfb']
                capacity_ones = 1
                capacity_hundreth = rongcapacity * capacity_ones
                capacity_hundreth = int(capacity_hundreth)

                medicineshfbid = []

                if changeupdate == "true":
                    electsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)
                    section_id2 = electsection[2]["section_id"]
                    db.execute("UPDATE section SET note = :noteshfb, sectionblock = :shfb WHERE section_id = :section_id2", noteshfb = noteshfb, shfb = shfb, section_id2 = section_id2)

                else:
                    sectionno = db.execute("INSERT INTO section (session_id,note, sectionblock) VALUES(?,?,?)",sessionno, noteshfb,shfb)


                ptbdays = db.execute("SELECT test_number FROM test ORDER BY test_id ASC LIMIT 2")
                ptbcounterr = 0
                ptbdayslistshfb = []
                ptbidlistshfb = []
                dateptbshfb = datefhfb + timedelta(days = 1)
                dayshfb = 0
                dayfhfb = dayfhfb + 1
                if changeupdate == "true":
                    db.execute("DELETE FROM calendar WHERE section_id = :section_id", section_id = section_id2)
                    pluster = 0
                    for i in range(shfb):
                        dateshfb  = datefhfb + timedelta(i + 1)
                        dayshfb = dayfhfb + i
                        eccalendar = 1.0
                        literperday = 1.0
                        if dayshfb > 20 and dayshfb < 25:
                            eccalendar = 1.2
                            literperday = 1.0
                        if dayshfb > 24 and dayshfb < 29:
                            eccalendar = 1.8
                            literperday = 1.0
                        if dayshfb > 28 and dayshfb < 61:
                            eccalendar = 2.0
                            literperday = 1.6
                        if dayshfb > 60:
                            eccalendar = 1.5
                            literperday = 1.2
                        db.execute("INSERT INTO calendar (section_id, date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)", section_id2, dateshfb, literperday, capacity_hundreth,ratio1shfb, ratio2shfb, ratioshfb, dayshfb, eccalendar)


                else:
                    for i in range(shfb):
                        dateshfb  = datefhfb + timedelta(i + 1)
                        dayshfb = dayfhfb + i
                        eccalendar = 1.0
                        literperday = 1.0
                        if dayshfb > 20 and dayshfb < 25:
                            eccalendar = 1.2
                            literperday = 1.0
                        if dayshfb > 24 and dayshfb < 29:
                            eccalendar = 1.8
                            literperday = 1.0
                        if dayshfb > 28 and dayshfb < 61:
                            eccalendar = 2.0
                            literperday = 1.6
                        if dayshfb > 60:
                            eccalendar = 1.5
                            literperday = 1.2
                        db.execute("INSERT INTO calendar (section_id, date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)", sectionno, dateshfb, literperday, capacity_hundreth,ratio1shfb, ratio2shfb, ratioshfb, dayshfb, eccalendar)




    #FHSB----------------------------------------------------------------------------
                fhsb = request.json['fhsb']
                fhsb = int(fhsb)
                ratiofhsb = request.json['ratiofhsb']
                ratio1fhsb = "1:1"
                ratio2fhsb = "50:50"
                notefhsb = request.json['notefhsb']
                capacity_ones = 1
                capacity_hundreth = rongcapacity * capacity_ones
                capacity_hundreth = int(capacity_hundreth)



                medicinefhsbid = []
                if changeupdate == "true":
                    electsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)
                    section_id3 = electsection[3]["section_id"]
                    db.execute("UPDATE section SET note = :notefhsb, sectionblock = :fhsb WHERE section_id = :section_id3", notefhsb = notefhsb, fhsb = fhsb, section_id3 = section_id3)

                else:
                    sectionno = db.execute("INSERT INTO section (session_id,note, sectionblock) VALUES(?,?,?)",sessionno, notefhsb,fhsb)



                fhsb = int(fhsb)

                ptbdays = db.execute("SELECT test_number FROM test ORDER BY test_id DESC LIMIT 2")
                ptbcounterr = 0
                ptbdayslistfhsb = []
                ptbidlistfhsb = []
                dateptbfhsb = dateshfb + timedelta(days = 1)



                dayfhsb = 0
                dayshfb = dayshfb + 1
                if changeupdate == "true":
                    db.execute("DELETE FROM calendar WHERE section_id = :section_id", section_id = section_id3)
                    pluster = 0
                    for i in range(fhsb):
                        datefhsb = dateshfb + timedelta(i + 1)
                        dayfhsb = dayshfb + i
                        eccalendar = 1.0
                        literperday = 1.0
                        if dayfhsb > 20 and dayfhsb < 25:
                            eccalendar = 1.2
                            literperday = 1.0
                        if dayfhsb > 24 and dayfhsb < 29:
                            eccalendar = 1.8
                            literperday = 1.0
                        if dayfhsb > 28 and dayfhsb < 61:
                            eccalendar = 2.0
                            literperday = 1.6
                        if dayfhsb > 60:
                            eccalendar = 1.5
                            literperday = 1.2
                        db.execute("INSERT INTO calendar (section_id, date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)", section_id3, datefhsb, literperday, capacity_hundreth,ratio1fhsb, ratio2fhsb, ratiofhsb, dayfhsb, eccalendar)

                else:
                    for i in range(fhsb):
                        datefhsb = dateshfb + timedelta(i + 1)
                        dayfhsb = dayshfb + i
                        eccalendar = 1.0
                        literperday = 1.0
                        if dayfhsb > 20 and dayfhsb < 25:
                            eccalendar = 1.2
                            literperday = 1.0
                        if dayfhsb > 24 and dayfhsb < 29:
                            eccalendar = 1.8
                            literperday = 1.0
                        if dayfhsb > 28 and dayfhsb < 61:
                            eccalendar = 2.0
                            literperday = 1.6
                        if dayfhsb > 60:
                            eccalendar = 1.5
                            literperday = 1.2
                        db.execute("INSERT INTO calendar (section_id, date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)", sectionno, datefhsb, literperday, capacity_hundreth,ratio1fhsb, ratio2fhsb, ratiofhsb, dayfhsb, eccalendar)


    #SHSB-----------------------------------------------------------------------------
                shsb = request.json['shsb']
                shsb = int(shsb)
                ratioshsb = request.json['ratioshsb']
                ratio1shsb = "0.5.1:25"
                ratio2shsb = "29:71"
                noteshsb = request.json['noteshsb']
                capacity_ones = 1
                capacity_hundreth = rongcapacity * capacity_ones
                capacity_hundreth = int(capacity_hundreth)


                medicineshsbid = []
                if changeupdate == "true":
                    electsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)
                    section_id4 = electsection[4]["section_id"]
                    db.execute("UPDATE section SET note = :noteshsb,sectionblock = :shsb WHERE section_id = :section_id4", noteshsb = noteshsb, shsb = shsb, section_id4 = section_id4)
                else:
                    sectionno = db.execute("INSERT INTO section (session_id,note,sectionblock) VALUES(?,?,?)",sessionno, noteshsb,shsb)


                shsb = int(shsb)
                ptbdays = db.execute("SELECT test_number FROM test ORDER BY test_id DESC LIMIT 2")
                ptbcounterr = 0
                ptbdayslistshsb = []
                ptbidlistshsb = []
                dateptbshsb = datefhsb + timedelta(days = 1)


                dayshsb = 0
                dayfhsb = dayfhsb + 1

                if changeupdate == "true":
                    db.execute("DELETE FROM calendar WHERE section_id = :section_id", section_id = section_id4)
                    pluster = 0
                    for i in range(shsb):
                        dateshsb = datefhsb + timedelta(i + 1)
                        dayshsb = dayfhsb + i
                        eccalendar = 1.0
                        literperday = 1.0
                        if dayshsb > 20 and dayshsb < 25:
                            eccalendar = 1.2
                            literperday = 1.0
                        if dayshsb > 24 and dayshsb < 29:
                            eccalendar = 1.8
                            literperday = 1.0
                        if dayshsb > 28 and dayshsb < 61:
                            eccalendar = 2.0
                            literperday = 1.6
                        if dayshsb > 60:
                            eccalendar = 1.5
                            literperday = 1.2
                        db.execute("INSERT INTO calendar (section_id, date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)", section_id4, dateshsb, literperday, capacity_hundreth,ratio1shsb, ratio2shsb, ratioshsb, dayshsb, eccalendar)

                else:
                    for i in range(shsb):
                        dateshsb = datefhsb + timedelta(i + 1)
                        dayshsb = dayfhsb + i
                        eccalendar = 1.0
                        literperday = 1.0
                        if dayshsb > 20 and dayshsb < 25:
                            eccalendar = 1.2
                            literperday = 1.0
                        if dayshsb > 24 and dayshsb < 29:
                            eccalendar = 1.8
                            literperday = 1.0
                        if dayshsb > 28 and dayshsb < 61:
                            eccalendar = 2.0
                            literperday = 1.6
                        if dayshsb > 60:
                            eccalendar = 1.5
                            literperday = 1.2
                        db.execute("INSERT INTO calendar (section_id, date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)", sectionno, dateshsb, literperday, capacity_hundreth,ratio1shsb, ratio2shsb, ratioshsb, dayshsb, eccalendar)



    #THSB-----------------------------------------------------------------------------
                thsb = request.json['thsb']
                thsb = int(thsb)
                ratiothsb = request.json['ratiothsb']
                ratio1thsb = "1"
                ratio2thsb = "1"
                notethsb = request.json['notethsb']
                capacity_ones = 1.5
                capacity_hundreth = rongcapacity * capacity_ones
                capacity_hundreth = int(capacity_hundreth)



                medicinethsbid = []
                if changeupdate == "true":
                    electsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)
                    section_id5 = electsection[5]["section_id"]
                    db.execute("UPDATE section SET note = :notethsb,sectionblock = :thsb WHERE section_id = :section_id5", notethsb = notethsb,thsb = thsb, section_id5 = section_id5)
                else:
                    sectionno = db.execute("INSERT INTO section (session_id,note,sectionblock) VALUES(?,?,?)",sessionno, notethsb,thsb)

                thsb = int(thsb)
                ptbdays = db.execute("SELECT test_number FROM test ORDER BY test_id DESC LIMIT 2")
                ptbcounterr = 0
                ptbdayslistthsb = []
                ptbidlistthsb = []
                dateptbthsb = dateshsb + timedelta(days = 1)


                dayshsb = dayshsb + 1
                if changeupdate == "true":
                    db.execute("DELETE FROM calendar WHERE section_id = :section_id", section_id = section_id5)
                    pluster = 0
                    for i in range(thsb):
                        datethsb = dateshsb + timedelta(i + 1)
                        daythsb = dayshsb + i
                        eccalendar = 1.0
                        literperday = 1.0
                        if daythsb > 20 and daythsb < 25:
                            eccalendar = 1.2
                            literperday = 1.0
                        if daythsb > 24 and daythsb < 29:
                            eccalendar = 1.8
                            literperday = 1.0
                        if daythsb > 28 and daythsb < 61:
                            eccalendar = 2.0
                            literperday = 1.6
                        if daythsb > 60:
                            eccalendar = 1.5
                            literperday = 1.2
                        db.execute("INSERT INTO calendar (section_id, date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)", section_id5, datethsb, literperday, capacity_hundreth,ratio1thsb, ratio2thsb, ratiothsb, daythsb, eccalendar)
                else:
                    for i in range(thsb):
                        datethsb = dateshsb + timedelta(i + 1)
                        daythsb = dayshsb + i
                        eccalendar = 1.0
                        literperday = 1.0
                        if daythsb > 20 and daythsb < 25:
                            eccalendar = 1.2
                            literperday = 1.0
                        if daythsb > 24 and daythsb < 29:
                            eccalendar = 1.8
                            literperday = 1.0
                        if daythsb > 28 and daythsb < 61:
                            eccalendar = 2.0
                            literperday = 1.6
                        if daythsb > 60:
                            eccalendar = 1.5
                            literperday = 1.2
                        db.execute("INSERT INTO calendar (section_id, date, literperday, litermellon, ratio_ones, ratio_hundreth, ratio, day, eccalendar) VALUES(?,?,?,?,?,?,?,?,?)", sectionno, datethsb, literperday, capacity_hundreth,ratio1thsb, ratio2thsb, ratiothsb, daythsb, eccalendar)


                fb = request.json['fb']
                sb = request.json['sb']







            if 'assumptionid' in request.json.keys():
                assumptionid = request.json['assumptionid']

                if assumptionid != "":
                    assumption = db.execute("SELECT * FROM assumption WHERE assumptionkey = :assumptionid", assumptionid = assumptionid)
                    assumptionname = assumption[0]["assumption_name"]
                    seedspeciesname = assumption[0]["seedspeciesname_ass"]
                    startdate = assumption[0]["startdate_ass"]
                    longtoong = assumption[0]["longtoong_ass"]

                    medicine = assumption[0]["medicine_ass"]
                    fb = assumption[0]["fb_ass"]
                    sb = assumption[0]["sb_ass"]
                    fhfb = assumption[0]["fhfb_ass"]
                    shfb = assumption[0]["shfb_ass"]
                    fhsb = assumption[0]["fhsb_ass"]
                    shsb = assumption[0]["shsb_ass"]
                    thsb = assumption[0]["thsb_ass"]
                    ratiofhfb = assumption[0]["ratiofhfb_ass"]
                    ratioshfb = assumption[0]["ratioshfb_ass"]
                    ratiofhsb = assumption[0]["ratiofhsb_ass"]
                    ratioshsb = assumption[0]["ratioshsb_ass"]
                    ratiothsb = assumption[0]["ratiothsb_ass"]

                    notefhfb = assumption[0]["note_fhfb_ass"]
                    noteshfb = assumption[0]["note_shfb_ass"]
                    notefhsb = assumption[0]["note_fhsb_ass"]
                    noteshsb = assumption[0]["note_shsb_ass"]
                    notethsb = assumption[0]["note_thsb_ass"]
                    return ({'seedspeciesnamee': seedspeciesname, 'assumptionname': assumptionname,'longtoong':longtoong, 'fb': fb, 'sb': sb, 'fhfb': fhfb, 'shfb': shfb, 'fhsb':fhsb, 'shsb':shsb, 'thsb': thsb,
                    'ratiofhfb': ratiofhfb, 'ratioshfb':ratioshfb, 'ratiofhsb': ratiofhsb, 'ratioshsb': ratioshsb, 'ratiothsb': ratiothsb, 'notefhfb': notefhfb, 'noteshfb': noteshfb, 'notefhsb': notefhsb,
                    'noteshsb': noteshsb, 'notethsb': notethsb, 'medicine': medicine}, 200, {'ContentType':'application/json'})


            if 'id' in request.json.keys():
                forselectss = request.json['id']
                if forselectss != "":
                    secondblock = db.execute("SELECT * FROM seedspecies WHERE seedspecies_id = :forselectss", forselectss = forselectss)
                    secondblockk = secondblock[0]["secondblocknumdays"]
                    seedspecies = secondblock[0]["seedspecies_id"]

                    return ({'id':secondblockk, 'seedspecies': seedspecies} ,200, {'ContentType':'application/json'})


            if 'checkforsave' in request.json.keys():
                checkforsave = request.json['checkforsave']
                return ({'checkforsave':checkforsave} ,200, {'ContentType':'application/json'})


    for row in seedddspecies:
        seedddspeciess = seedddspecies[counter]["seedspecies_name"]
        optionseedspeciesid = seedddspecies[counter]["seedspecies_id"]
        itemsrow = dict(seedddspeciess = seedddspeciess, optionseedspeciesid = optionseedspeciesid)
        itemsddseedspecies.append(itemsrow)
        counter+=1
    counter = 0
    for row in ptbdd:
        ptbddd = ptbdd[counter]["ratiomed"]
        optionptbid = ptbdd[counter]["ptb_id"]
        itemsrow = dict(ptbddd = ptbddd, optionptbid = optionptbid)
        itemsptbdd.append(itemsrow)

        counter+=1

    counter = 0

    counter = 0
    for row in medicinedd:
        medicineddd = medicinedd[counter]["medicine_name"]
        optionmedicineid = medicinedd[counter]["medicine_id"]
        itemsrow = dict(medicineddd = medicineddd, optionmedicineid = optionmedicineid)
        itemsmedicinedd.append(itemsrow)

        counter+=1

    counter = 0
    for row in assumptioninform:
        assumption = assumptioninform[counter]["assumption_name"]
        assumptionkey = assumptioninform[counter]["assumptionkey"]
        itemsrow = dict(assumption = assumption, assumptionkey = assumptionkey)
        itemsassumption.append(itemsrow)
        counter+=1



    db.execute("SELECT * FROM rong WHERE rong_id = :rong_id", rong_id = rong_id)
    selectsession = db.execute("SELECT MAX(session_id) AS session_id, seedspecies_id,sessionname,medicinesession,beforelongtoong,assumption_val FROM session WHERE rong_id = :rong_id", rong_id = rong_id)
    sessiondo = db.execute("SELECT MAX(session_id) AS session_id FROM session")
    sessiondi = sessiondo[0]["session_id"]
    if sessiondi == None:
        sessiondi = 1
    else:
        sessiondi = sessiondi + 1


    if selectsession[0]["session_id"] != None:


    ###################################

        session_id = selectsession[0]["session_id"]
        seedspecies_id = selectsession[0]["seedspecies_id"]
        longtoongdays = selectsession[0]["beforelongtoong"]
        selectwhatever = db.execute("SELECT * FROM seedspecies WHERE seedspecies_id = :seedspecies_id",seedspecies_id = seedspecies_id)
        seedspecies_name = selectwhatever[0]["seedspecies_name"]
        longtoongdays = int(longtoongdays)

        selectmed = selectsession[0]["medicinesession"]
        assumption_val = selectsession[0]["assumption_val"]

        selectmed = selectmed.split("'")
        itemsselectmed = []
        for i in selectmed:
            med = i
            ye = dict(med = med)
            itemsselectmed.append(ye)

        itemsednumfhfb = []
        itemsednumshfb = []
        itemsednumfhsb = []
        itemsednumshsb = []
        itemsednumthsb = []

        electsection = db.execute("SELECT * FROM section WHERE session_id = :session_id", session_id = session_id)


        fhfbb = electsection[1]["sectionblock"]

        shfbb = electsection[2]["sectionblock"]
        fhsbb = electsection[3]["sectionblock"]
        shsbb = electsection[4]["sectionblock"]
        thsbb = electsection[5]["sectionblock"]



        section_id = electsection[0]["section_id"]
        section_id1 = electsection[1]["section_id"]
        section_id2 = electsection[2]["section_id"]
        section_id3 = electsection[3]["section_id"]
        section_id4 = electsection[4]["section_id"]
        section_id5 = electsection[5]["section_id"]



        counteredn = 0
        selectstartdate = db.execute("SELECT * FROM calendar WHERE section_id = :section_id", section_id = section_id)
        selectstartdate1 = db.execute("SELECT * FROM calendar WHERE section_id = :section_id", section_id = section_id1)
        selectstartdate2 = db.execute("SELECT * FROM calendar WHERE section_id = :section_id", section_id = section_id2)
        selectstartdate3 = db.execute("SELECT * FROM calendar WHERE section_id = :section_id", section_id = section_id3)
        selectstartdate4 = db.execute("SELECT * FROM calendar WHERE section_id = :section_id", section_id = section_id4)
        selectstartdate5 = db.execute("SELECT * FROM calendar WHERE section_id = :section_id", section_id = section_id5)

        newstartdate = selectstartdate[0]["date"]
        newstartdatefb = selectstartdate1[0]["date"]
        newstartdatefhfb = selectstartdate1[0]["date"]
        newstartdateshfb = selectstartdate2[0]["date"]
        newstartdatesb = selectstartdate3[0]["date"]
        newstartdatefhsb = selectstartdate3[0]["date"]
        newstartdateshsb = selectstartdate4[0]["date"]
        newstartdatethsb = selectstartdate5[0]["date"]
        laststartdate = selectstartdate5[-1]["date"]




        fbb = int(fhfbb) + int(shfbb)
        sbb = int(fhsbb) + int(shsbb) + int(thsbb)

        nfhfbb = electsection[1]["note"]
        nshfbb = electsection[2]["note"]
        nfhsbb = electsection[3]["note"]
        nshsbb = electsection[4]["note"]
        nthsbb = electsection[5]["note"]



        sessionnamee= selectsession[0]["sessionname"]


        return render_template("information.html", itemsddseedspecies = itemsddseedspecies, itemsmedicinedd = itemsmedicinedd, itemsptbdd = itemsptbdd, rongname = rongname, fhfbb = fhfbb, shfbb = shfbb, fhsbb = fhsbb, shsbb = shsbb, thsbb = thsbb
        ,nfhfbb = nfhfbb, nshfbb = nshfbb, nfhsbb = nfhsbb, nshsbb = nshsbb, nthsbb = nthsbb, fbb = fbb, sbb = sbb, itemsednumfhfb = itemsednumfhfb, itemsednumshfb = itemsednumshfb,
        itemsednumfhsb = itemsednumfhsb, itemsednumshsb = itemsednumshsb, itemsednumthsb = itemsednumthsb, seedspecies_name = seedspecies_name, sessionnamee = sessionnamee, newstartdate = newstartdate, newstartdatefb = newstartdatefb, newstartdatefhfb = newstartdatefhfb,newstartdateshfb = newstartdateshfb,
        newstartdatesb = newstartdatesb, newstartdatefhsb = newstartdatefhsb, newstartdateshsb = newstartdateshsb, newstartdatethsb = newstartdatethsb,
        itemsnothing = itemsnothing, itemsselectmed = itemsselectmed, longtoongdays = longtoongdays, laststartdate = laststartdate, itemsassumption = itemsassumption, assumption_val = assumption_val,session_id = sessiondi, changeupdate = changeupdate)

    else:
        return render_template("information.html", itemsddseedspecies = itemsddseedspecies, itemsmedicinedd = itemsmedicinedd, itemsptbdd = itemsptbdd, rongname = rongname, itemsassumption = itemsassumption, session_id = sessiondi)







@app.route("/management", methods=["GET", "POST"])
def management():
    itemsSEEDSPECIES = []
    items2NDBLOCKNUMDAYS = []
    itemsEC = []
    itemsPTB = []
    itemsMEDICINE = []
    itemsSEEDSPECIESID = []




    today = date.today()
    showalltoday = today.strftime("%B %d, %Y")

    if request.method == "POST":

        #CHECK IF USER PUT IN ALL THE REQUIRED INFO OR Not

        if request.content_type == "application/json":

            formanagement = request.json['id']
            formanagement = formanagement.split("_")
            lastchar = formanagement[1]



            formanagementchar = request.json['char4']


            if formanagementchar == "s":
                db.execute("UPDATE seedspecies SET booleanseedspecies = 0 WHERE seedspecies_id = :lastchar", lastchar = lastchar)

            if formanagementchar == "p":
                db.execute("UPDATE ptb SET booleanptb = 0 WHERE ptb_id = :lastchar", lastchar = lastchar)
            if formanagementchar == "m":
                db.execute("UPDATE medicine SET booleanmedicine = 0 WHERE medicine_id = :lastchar", lastchar = lastchar)


        #if not request.form.get("seedspeciesname1"):
            #if not request.form.get("seedspeciesday"):
             #   if not request.form.get("medicinename1"):
                 #   if not request.form.get("ec1"):
                      #  if not request.form.get("ptb1"):
                            #return ("fill in atleast one form before saving")


        #GET THE VALUE OF TEXT USER PUT IN
        seedspecies = request.form.getlist("seedspeciesname1")
        secondblocknumdays = request.form.getlist("seedspeciesday")
        medicinename = request.form.getlist("medicinename1")
        print(f"medicinename: {medicinename}")
        print(f"seedspeices: {seedspecies}")
        print(f"secondblocknumdays: {secondblocknumdays}")


        ec = request.form.getlist("ec1")
        ptbratio = request.form.getlist("ptb1")
       # if medicinename == "":
         #   print("aw man failed")
        #if medicinename != "":

        #PUT ALL THE VALUE INTO DATABASE

        for i,h in zip(seedspecies,secondblocknumdays):
            one = 1
            if i != "" and h != "":
                db.execute("INSERT INTO seedspecies (seedspecies_name, secondblocknumdays, booleanseedspecies ) VALUES(?,?,?)", i,h, one)

        for j in medicinename:
            one = 1
            if j != "":
                db.execute("INSERT INTO medicine (medicine_name, booleanmedicine) VALUES(?,?)", j, one)

        for p in ptbratio:
            one = 1
            if p != "":
                db.execute("INSERT INTO ptb (ratiomed, booleanptb) VALUES(?,?)", p, one)
     #SELECT INFORMATION FROM DATABASE

    seedspeciesdb = db.execute("SELECT seedspecies_id, seedspecies_name, secondblocknumdays FROM seedspecies WHERE booleanseedspecies = 1")
    ratiomedfromdb = db.execute("SELECT ptb_id, ratiomed FROM ptb WHERE booleanptb = 1")
    medicinefromdb = db.execute("SELECT medicine_id, medicine_name FROM medicine WHERE booleanmedicine = 1")

    #if list is empty so that error ja dai mai gerd
    if not ratiomedfromdb:
        return render_template("management.html")

    if not seedspeciesdb:
        return render_template("management.html")
    #if not sbndfromdb:
      #  return render_template("management.html")
    if not medicinefromdb:
        return render_template("management.html")


    #SHOW THE INFORMATION TO THE VALUE

    counter = 0
    for row in seedspeciesdb:
        ssnfromdbb = seedspeciesdb[counter]["seedspecies_name"]
        nseedspecies = "naaw" + str(counter)
        divseed = "divseed" + "_" + str(seedspeciesdb[counter]["seedspecies_id"])
        sbndfromdbb = seedspeciesdb[counter]["secondblocknumdays"]
        nseedspecies = "naaw" + str(counter)
        button = "b" + str(counter)
        itemsrow = dict(sbndfromdbb = sbndfromdbb, nseedspecies = nseedspecies,  button = button,
        ssnfromdbb = ssnfromdbb, divseedd = divseed)
        itemsSEEDSPECIES.append(itemsrow)
        counter+=1


    counter=0

    for row in ratiomedfromdb:
        ratiomedfromdbb = ratiomedfromdb[counter]["ratiomed"]
        nratiomed = "nratio" + ratiomedfromdbb
        dividptb = "divptb_" + str(ratiomedfromdb[counter]["ptb_id"])
        itemsrow = dict(ratiomedfromdbb = ratiomedfromdbb, nratiomed = nratiomed, divptb = dividptb)
        itemsPTB.append(itemsrow)
        counter+=1

    counter=0
    for row in medicinefromdb:
        medicinefromdbb = medicinefromdb[counter]["medicine_name"]
        nmedicinename = "nmed" + medicinefromdbb
        divid = "divmed_" + str(medicinefromdb[counter]["medicine_id"])
        itemsrow = dict(medicinefromdbb = medicinefromdbb, nmedicinename = nmedicinename, divid = divid)
        itemsMEDICINE.append(itemsrow)
        counter+=1

    counter = 0



    return render_template("management.html", today = showalltoday,
    itemsSEEDSPECIES = itemsSEEDSPECIES, itemsPTB = itemsPTB, itemsEC = itemsEC, itemsMEDICINE = itemsMEDICINE, items2NDBLOCKNUMDAYS = items2NDBLOCKNUMDAYS, itemsSEEDSPECIESID = itemsSEEDSPECIESID)




@app.route("/creatingrong", methods=["GET", "POST"])
def creatingrong():
    today = date.today()
    showalltoday = today.strftime("%B %d, %Y")
    if request.method == "POST":
        if request.content_type == "application/json":
            if 'checker' in request.json.keys():
                return render_template("creatingrong.html")
            else:
                rongname = request.json['rongname']
                rongcapacity = request.json['rongcapacity']
                print(rongname)
                print(rongcapacity)
                db.execute("INSERT INTO rong (rong_name,rong_capacity) VALUES(?,?)", rongname,rongcapacity)
        return redirect("/rong")

    return render_template("creatingrong.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("raviapology.html")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)



