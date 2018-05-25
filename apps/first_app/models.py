from django.db import models
import bcrypt,datetime


class UserManager(models.Manager):
    def validate_registration(self, postData):
        response = {
           'status' : False,
           'errors' : []
        }
        if len(postData['name']) < 2:
           response['errors'].append("Name too short")

        # if User.objects.filter(alias=postData['alias']).count() > 0:
        #     response['errors'].append(f"Alias {postData['alias']} already exists")
        if len(postData['alias']) <3:
            response['errors'].append("alias must be at least 3 characters")

        if len(postData['username']) < 9:
           response['errors'].append("Invalid Email")

        if len(postData['password']) < 8:
            response['errors'].append("Invalid Password")

        if postData['confirm_pw'] != postData['password']:
            response['errors'].append("Invalid Password")

        if len(postData['date']) > 0:
            today = datetime.datetime.today()
            date = datetime.datetime.strptime(postData['date'], '%Y-%m-%d')
            if date > today:
                response['errors'].append(' BirthDate cannot be in the future')
        if len(postData['date']) < 1:
            response['errors'].append('Date of Birth required')
    

        if len(response['errors']) == 0:
            response['status'] = True
            response['user_id'] = User.objects.create(
                name=postData['name'],
                alias=postData['alias'],
                username=postData['username'],
                date=postData['date'],
                password=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            ).id
        return response 

    def validate_login(self, postData):
        response = {
           'status' : False,
           'errors' : []
        }
        #if len(User.objects.filter(eamil=postData['email'])) == 0:
        existing_users = User.objects.filter(username=postData['username'])
        if len(existing_users) == 0:
            response['errors'].append("invalid input")
        else:
            if bcrypt.checkpw(postData['password'].encode(), existing_users[0].password.encode()):
                response['status'] = True
                response['user_id'] = existing_users[0].id
            else:
                response['errors'].append("invalid input")
        return response  


class QuoteManager(models.Manager):
    def validate_submit(self,postData,user_id):
        response = {
            "status" : False,
            "errors": []
        }
        if len(postData['quoted_by']) == 0:
            response['errors'].append("quoted_by cannot be empty")
        if len(postData['quoted_by']) < 3:
            response['errors'].append("quoted_by should be atleast 3 characters")

        if len(postData['message']) < 10:
            response['errors'].append("message should be atleast 10 characters")

        if len(response['errors']) == 0:
            response['status'] = True
            posted_by = User.objects.get(id=user_id)
            quote = Quote.objects.create(
                quoted_by=postData['quoted_by'],
                message=postData['message'],
                posted_by = User.objects.get(id=user_id)
            )
            # quote.others.add(posted_by)
            # quote.save()
        return response

    def add(self, quote_id, user_id):
        me = User.objects.get(id=user_id)
        quote = Quote.objects.get(id=quote_id)
        quote.others.add(me) 
        quote.save() 

    def remove(self, quote_id, user_id):
        me = User.objects.get(id=user_id)
        quote = Quote.objects.get(id=quote_id)
        quote.others.remove(me) 
        quote.save() 


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()




class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    posted_by = models.ForeignKey(User, related_name="added_quotes", null=True)
    others= models.ManyToManyField(User, related_name="quotes", null=True)
    objects = QuoteManager()