from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify,flash
from functools import wraps
import random

from twilio.rest import Client
from .. import keys
client = Client(keys.account_sid, keys.auth_token)

from ..models import *

user = Blueprint('user', __name__ , static_folder="static", template_folder="templates")


def is_user_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'id' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('hom.home'))
    return wrap


@user.route('/dna', methods=['GET','POST'])
@is_user_in
def dna():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        email = request.form.get('email')
        number = request.form.get('number')
        residence = request.form.get('residence')
        reason = request.form.get('reason')
        
        record = DnaTest(user_id=session['id'],first_name=f_name,last_name=l_name,email=email,contact_number=number,residence=residence,reason=reason)
        db.session.add(record)
        db.session.commit()

        return redirect(url_for('user.profile'))

    id = session['id']
    user = Users.query.filter_by(id=id).first()
    return render_template('user/dna.html', user = user)

@user.route('/bio', methods=['GET','POST'])
@is_user_in
def biography():
    if request.method == "POST":
        bio = request.form.get('bio')
        profile = Profile.query.filter_by(id=session['id']).first()
        if profile:
            print("naughty.")
            profile.biography = bio
            db.session.commit()
            return redirect(url_for('user.profile'))
        flash('First complete your profile.!')
        return redirect(url_for('user.biography'))
        
    id = session['id']
    user = Users.query.filter_by(id=id).first()
    return render_template('user/bio.html', user = user)

@user.route('/', methods=["GET","POST"])
@is_user_in
def profile():
    if Profile.query.filter_by(uid=session['id']).first() and FamilyDetails.query.filter_by(uid=session['id']).first():
        person = Users.query.filter_by(id=session['id']).first()
        profile = Profile.query.filter_by(uid=session['id']).first()
        family = FamilyDetails.query.filter_by(uid=session['id']).first()
        
        return render_template('user/profile.html',done=True,person=person, profile = profile, family=family)
    
    if request.method =="POST":
        gotra = request.form.get('gotra')
        religion = request.form.get('religion')
        caste = request.form.get('caste')
        s_caste = request.form.get('sub_caste')
        native_town = request.form.get('native_town')
        mother_tongue = request.form.get('mother_tongue')
        place_of_birth = request.form.get('place_of_birth')
        dob = request.form.get('dob')
        gender = request.form.get('gender')

        prof = Profile(uid = session['id'],gotra = gotra.lower(), religion=religion.lower(), caste=caste.lower(),gender=gender.lower(),sub_caste=s_caste.lower(),mother_tongue=mother_tongue.lower(),native_region=native_town.lower(),date_of_birth=dob,place_of_birth=place_of_birth.lower())
        db.session.add(prof)

        father_name = request.form.get('father_name')
        mother_name = request.form.get('mother_name')
        grand_father = request.form.get('grand_father')
        grand_mother = request.form.get('grand_mother')
        g_grand_father =''   #g_grand_father = request.form.get('g_grand_father')
        g_grand_mother =''     #g_grand_mother = request.form.get('g_grand_mother')
        spouse_name = request.form.get('spouse_name')
        kid = request.form.getlist('kid')

        kids = ""
        if kid:
            for k in kid:
                try:
                    kids = kids + "," +k.lower()
                except:
                    kids = k.lower()
        else:
            kids = None
        
        fam = FamilyDetails(uid=session['id'],father_name=father_name.lower(),mother_name=mother_name.lower(),
        grand_father=grand_father.lower(),grand_mother=grand_mother.lower(),great_grand_father=g_grand_father.lower(),great_grand_mother=g_grand_mother.lower(),spouse_name=spouse_name.lower(),kids=kids)

        db.session.add(fam)
        db.session.commit()

    return render_template('user/profile.html')

@user.route('/dashboard')
@is_user_in
def dashboard():
    id = session['id']
    me=Users.query.filter_by(id=id).first()
    frds = me.family_users
    if frds is not None:
        frs=[]
        req = []
        for i in frds.split(','):
            if i[-1] != '+':
                r = Users.query.filter_by(id=int(i)).first()
                req.append({'id':i,'name':r.sur_name+' '+r.first_name+' '+r.last_name})
            else:
                r = Users.query.filter_by(id=int(i[:-1])).first()
                frs.append({'id':i,'name':r.sur_name+' '+r.first_name+' '+r.last_name})
                frs.append(i)
    else:
        frs =None
        req=None
    return render_template('user/dashboard.html', user = True, friends=frs, requests=req)


@user.route('/contact', methods=['GET','POST'])
@is_user_in
def contact():
    if request.method == "POST":
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        number = request.form.get('number')
        email = request.form.get('email')
        message = request.form.get('message')

        record = Contact(user_id=session['id'],first_name=f_name,last_name=l_name,contact_number=number,email=email,message=message)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('user.profle'))
    return render_template('user/contact.html', user = True)


@user.route('/about')
@is_user_in
def about():
    return render_template('user/about.html')

@user.route('/logout')
@is_user_in
def logout():
    id = session['id']
    session.pop('id', None)
    return redirect(url_for('hom.home'))

@user.route('/add_friend', methods=['POST'])
@is_user_in
def add_friend():
    me = Users.query.filter_by(id=session['id']).first()
    name=me.first_name
    id = request.form.get('id')
    print(id)
    friend = Users.query.filter_by(id=id).first().phone_number
    msg = f"Hey, {name} has invited you to the family tree on our app. To view him visit https://domain-name.com/user/{id}"
    try:
        print(friend)
        client.messages.create(
            body=msg,   
            from_ = keys.my_number,
            to = '+91'+ friend
        )
        print("api done")
        try:
            me.family_users = me + ','+id
        except:
            me.family_users = ''+id
        db.session.commit()
    except:
        return jsonify({"error":"Your request is not sent!!"})
    return jsonify({"success":"Your request has been sent successfully!!"})

@user.route('/<int:i>')
@is_user_in
def get_friend(i):
    friend = Users.query.filter_by(id=i).first()
    peers =friend.family_users
    if str(session['id']) in peers.split(','):
        return render_template('user/friend_request.html', friend=friend)
    return redirect(url_for('user.profle'))

@user.route('/accept_friend', methods=["POST"])
@is_user_in
def accept_friend():
    id_ = request.form.get('id')
    me1 = Users.query.filter_by(id=session['id']).first()
    me = me1.family_users
    if me:
        me = id_+'+'
    else:
        me = me + ','+id_+'+'
    
    friend = Users.query.filter_by(id=id_).first()
    l = friend.family_users
    li = l.split(',')
    final_ = ''
    if li is not None:
        if ','+id_+',' in li:
            final_ = l.replace(','+id_+',',','+id_+'+,')
        elif id_+',' in li:
            final_ = l.replace(id_+',', id_+'+,')
        else:
            final_ = l.replace(','+id_, ','+id_+',')
    else:
        final_ = str(id_)+'+'
    l = final_

    try:
        me1.family_users = me1.family_users + me
    except:
        me1.family_users = me

    db.session.commit()
    
    return redirect(url_for('user.friend',friend_id=id_))

@user.route('/friend')
@is_user_in
def friend():
    if request.args['friend_id']:
        id_ = request.args['friend_id']
    elif request.form.get('friend_id'):
        id_ = request.form.get('friend_id')
    else:
        return redirect(url_for('user.profle'))
    friend = Users.query.filter_by(id=id_).first()
    return render_template('user/friend.html', friend=friend)

@user.route('/search', methods=["POST"])
def search():
    q = request.form.get('q')
    qq = f"%{q}%"
    ppl_sn = Users.query.filter(Users.first_name.like(qq)).all()
    suggestions = []
    for i in ppl_sn:
        suggestions.append([str(i.id),i.sur_name+" "+i.first_name + " "+i.last_name])
    '''
    user = Users.query.filter_by(id=session['id']).first()
    sn = user.sur_name
    if user.family_users is None:
        friends = []
    else:
        friends = user.family_users.split(',')
    suggestions = []
    for i in ppl_sn:
        if i.id == session['id'] or str(i.id) in friends:
            continue
        if i.sur_name == sn:
            suggestions.append([str(i.id),i.sur_name+" "+i.first_name + " "+i.last_name])
    go = Profile.query.filter_by(uid=session['id']).first()
    if go:
        go = go.gotra
        ppl_go = Profile.query.filter_by(gotra = go).all()
        for i in ppl_go:
            if i.id == session['id'] or str(i.id) in friends:
                continue
            f = Users.query.filter_by(id=i.uid).first()
            pp = str(i.id),f.sur_name+" "+f.first_name + " "+f.last_name
            if pp not in suggestions:
                suggestions.append(pp)
    '''
    return jsonify({'results': suggestions})

@user.route('/add_relation', methods=["POST"])
@is_user_in
def add_relation():
    iid = request.form.get('id_')
    f_name = request.form.get('f_name')
    dob = request.form.get('dob')
    place_ob = request.form.get('place_of_birth')
    gender = request.form.get('gender')
    relation_name = request.form.get('relation_name')

    if relation_name == "brother" or relation_name=="sister":
        level = '+0'
    elif relation_name == 'son' or relation_name=='daughter':
        level = '-1'
    elif relation_name == "grand son" or relation_name == "grand daughter":
        level = '-2'
    elif relation_name == 'father' or relation_name == 'mother' or relation_name == 'uncle' or relation_name == 'aunty':
        level = '+1'
    elif relation_name == "grand father" or relation_name == "grand mother":
        level = '+2'
    elif relation_name == "great grand father" or relation_name == "great grand mother":
        level = '+3'
    else:
        level += '+0'

    user = Users.query.filter_by(id=session['id']).first()
    
    rel = Users(sur_name=user.sur_name,first_name=f_name,last_name=user.last_name,date_of_birth=dob,place_of_birth=place_ob,gender=gender,relation_name=relation_name,added_by=user.id, parent_user=int(iid))
    db.session.add(rel)
    db.session.commit()
    try:
        for i in user.relations.split(','):
            if len(i.split('+'))>1:
                k=i.split('+')
                if int(k[0]) == int(iid):
                    iid_level = int(k[1])
                    break
            else:
                k=i.split('-')
                if int(k[0]) == int(iid):
                    iid_level = int('-'+k[1])
                    break
    except:
        iid_level = 0
    
    new_user = Users.query.filter_by(parent_user=int(iid)).all()[-1]

    iid_relations=Users.query.filter_by(id=int(iid)).first()
    try:
        iid_relations.relations += ','+str(new_user.id)+level
    except TypeError:
        iid_relations.relations = str(new_user.id)+level

    final_level = int(iid_level) + int(level)

    if int(iid)!=user.id:
        try:
            if final_level>=0:
                user.relations += ','+str(new_user.id)+'+'+str(final_level)
            else:
                user.relations += ','+str(new_user.id)+str(final_level)
        except TypeError:
            if final_level>=0:
                user.relations = str(new_user.id)+'+'+str(final_level)
            else:
                user.relations = str(new_user.id)+str(final_level)

    db.session.commit()
    
    return jsonify({'success':'Relation added.'})

@user.route('/delete_relation', methods=['POST'])
@is_user_in
def delete_relation():
    id_ = request.form.get('id_')
    user = Users.query.filter_by(id=session['id']).first()
    rel = Users.query.filter_by(id=id_).first()
    f = user.relations.split(',')
    for r in f:
        if id_ in r:
            f.remove(r)
            break
    f_ =''
    for r in f:
        f_ = f_+r+','
    f_ = f_[:-1]
    try:
        user.relations = f_
        db.session.delete(rel)
        db.session.commit()
    except:
        return jsonify({'error':'Relation is not removed'})
    return redirect(url_for('user.tree'))

@user.route('/tree')
@is_user_in
def tree():
    user = Users.query.filter_by(id=session['id']).first()
    us = user.relations
    relatives = {4:[],3:[],2:[],1:[],0:[user],-1:[],-2:[],-3:[],-4:[]}
    if us:
        for i in us.split(','):
            if len(i.split('+'))>1:
                id_ = int(i.split('+')[0])
                level = int(i.split('+')[1])
            else:
                id_ = int(i.split('-')[0])
                j=i.split('-')[1]
                level = int('-'+j)
            f = Users.query.filter_by(id=id_).first()
            relatives[level].append(f)
    return render_template('user/tree.html',user=user, relatives=relatives)


@user.route('/forgotpassword')
def forgot_password():
    return render_template('home/forgot_pass.html')

@user.route('/verify-number' , methods=['POST'])
def verify_number():
    number = request.form.get('number')
    found_number = Users.query.filter_by(phone_number=number).first()
    if found_number:
        print("found")
        name=found_number.first_name
        return jsonify({'success':name})
    print("not found")
    return jsonify({'error':'This number is not registered'})


@user.route('/generate-otp' , methods=['POST'])
def generate_otp():
    mynum = request.form.get('num')
    if len(mynum) == 10:
        otp = random.randint(100000,999999)
        '''
        try:
            client.messages.create(
                body=f"Your OTP for changing the password is {otp}",   
                from_ = keys.my_number,
                to = '+91'+ friend
            )
        except:
            return jsonify({'error':'OTP is not sent'})
        '''
        print(otp)
        return jsonify({'otp':otp,'success':'yes'})
    return jsonify({'error':'Invalid number'})

@user.route('/change-password' , methods=['POST'])
def change_password():
    mynum = request.form.get('numb')
    us = Users.query.filter_by(phone_number=mynum).first()
    return redirect(url_for('user.password_page', user=us))

@user.route('/password-change', methods=["GET","POST"])
def password_page():
    user = request.args.get('user')
    return render_template('home/pass_change.html', user=user)

@user.route('/password-changed' , methods=['POST'])
def password_changed():
    newpass = request.form.get('passw')
    id_ = request.form.get('id_')
    try:
        use = Users.query.filter_by(id=id_).first()
        use.password = newpass
        db.session.commit()
        return jsonify({'success':'Password is changed successfully.'})
    except:
        return jsonify({'error':'Unfortunately, password is not changed.'})

@user.route('/edit_personal', methods=['POST'])
def edit_personal():
    id_ = request.form.get('id_')
    s_name = request.form.get('esur_name')
    f_name = request.form.get('efirst_name')
    l_name = request.form.get('elast_name')
    email = request.form.get('eemail')
    me = Users.query.filter_by(id=int(id_)).first()

    if s_name:
        me.sur_name = s_name
    if f_name:
        me.first_name = f_name
    if l_name:
        me.last_name = l_name
    if email:
        me.email = email    
    try:
        db.session.commit()
    except:
        flash('Detail are not updated. Try again!')

    return redirect(url_for('user.profile'))

@user.route('/edit_profile', methods=['POST'])
def edit_profile():
    id_ = request.form.get('id_')
    gotra = request.form.get('egotra')
    religion = request.form.get('ereligion')
    caste = request.form.get('ecaste')
    sub_caste = request.form.get('esub_caste')
    mother_t = request.form.get('emother_tongue')
    native_region = request.form.get('enative_region')
    dob = request.form.get('edob')
    place_of_birth = request.form.get('eplace_of_birth')

    me = Users.query.filter_by(id=id_).first()

    if gotra:
        me.gotra = gotra
    if religion:
        me.religion = religion
    if caste:
        me.caste = caste
    if sub_caste:
        me.sub_caste = sub_caste
    if mother_t:
        me.mother_tongue = mother_t
    if native_region:
        me.native_region =native_region
    if dob:
        me.date_of_birth =dob
    if place_of_birth:
        me.place_of_birth =place_of_birth
    try:
        db.session.commit()
    except:
        flash('Detail are not updated. Try again!')
    
    return redirect(url_for('user.profile'))

@user.route('/edit_family', methods=['POST'])
def edit_family():
    id_ = request.form.get('id_')
    father_name = request.form.get('efather_name')
    mother_name = request.form.get('emother_name')
    g_father = request.form.get('eg_father')
    g_mother = request.form.get('eg_mother')
    gg_father = request.form.get('egg_father')
    gg_mother = request.form.get('egg_mother')
    spouse = request.form.get('espouse')
    kids = request.form.getlist('ekid')
    me = Users.query.filter_by(id=id_).first()

    if father_name:
        me.father_name = father_name
    if mother_name:
        me.mother_name = mother_name
    if g_father:
        me.grand_father = g_father
    if g_mother:
        me.grand_mother = g_mother  
    if gg_father:
        me.great_grand_father =  gg_father
    if gg_mother:
        me.great_grand_mother = gg_mother 
    if spouse:
        me.spouse =  spouse
    if kids:
        k = kids[0]
        for i in kids[1:]:
            k=','+k
        me.kids =  k
    try:
        db.session.commit()
    except:
        flash('Detail are not updated. Try again!')
    
    return redirect(url_for('user.profile'))