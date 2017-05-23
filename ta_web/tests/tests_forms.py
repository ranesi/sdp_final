from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.db import IntegrityError

import re

from text_analysis.ta_web.models import Document
from text_analysis.ta_web.forms import AddDocumentForm, CreateUserForm


class AddDocumentFormTest(TestCase):
    def setUp(self):
        User.objects.create(
            username='asd',
            password='zxcvzxcv'
        )

    def test_no_title(self):
        user = User.objects.get(username='asd')

        form_data = dict(
            text=getty,
            author=user
        )

        test_form = AddDocumentForm(form_data)

        self.assertFalse(test_form.is_valid())

    def test_no_body(self):
        user = User.objects.get(username='asd')

        form_data = dict(
            title=title,
            author=user
        )

        test_form = AddDocumentForm(form_data)

        self.assertFalse(test_form.is_valid())


class CreateUserFormTest(TestCase):
    def setUp(self):
        user1_info = dict(
            username='a',
            email='b@b.gov',
            password1='zxcvzxcv',
            password2='zxcvzxcv'
        )
        user2_info = dict(
            username='b',
            email='c@c.biz',
            password1='qwerqwer',
            password2='qwerqwer'
        )
        user1 = User(user1_info)
        user2 = User(user2_info)

        user1.save()
        user2.save()

    def valid_user_creation_form(self):
        test_data = dict(
            username='JimmyDean',
            email='breakfast@sausage.com',
            password1='egg$andwiches',
            password2='egg$andwiches'
        )
        test_form = CreateUserForm(test_data)
        self.assertTrue(test_form.is_valid())

    def password_too_short(self):
        test_data = dict(
            username='Bisquik',
            email='waffle@pancake.com',
            password1='asdfasd',
            password2='asdfasd'
        )
        test_form = CreateUserForm(test_data)
        self.assertFalse(test_form.is_valid())

    def username_already_exists(self):
        test_data = dict(
            username='a',
            email='waffle@pancake.com',
            password1='zxcvzxcv',
            password2='zxcvzxcv'
        )
        test_form = CreateUserForm(test_data)
        self.assertFalse(test_form.is_valid())

    def username_case_insensitive(self):
        test_data = dict(
            username='A',
            email='waffle@pancake.biz',
            password1='zxcvzxcv',
            password2='zxcvzxcv'
        )
        test_form = CreateUserForm(test_data)
        self.assertFalse(test_form.is_valid())


# __END__

title = 'Test'

getty = '''
Four score and seven years ago our fathers brought forth on this continent, 
a new nation, conceived in Liberty, and dedicated to the proposition that 
all men are created equal.

Now we are engaged in a great civil war, testing whether that nation, 
or any nation so conceived and so dedicated, can long endure. We are met 
on a great battle-field of that war. We have come to dedicate a portion 
of that field, as a final resting place for those who here gave their 
lives that that nation might live. It is altogether fitting and proper 
that we should do this.

But, in a larger sense, we can not dedicate—we can not consecrate—we 
can not hallow—this ground. The brave men, living and dead, who struggled 
here, have consecrated it, far above our poor power to add or detract. 
The world will little note, nor long remember what we say here, but it 
can never forget what they did here. It is for us the living, rather, 
to be dedicated here to the unfinished work which they who fought here 
have thus far so nobly advanced. It is rather for us to be here dedicated 
to the great task remaining before us—that from these honored dead we 
take increased devotion to that cause for which they gave the last full
measure of devotion—that we here highly resolve that these dead shall
not have died in vain—that this nation, under God, shall have a new 
birth of freedom—and that government of the people, by the people,
for the people, shall not perish from the earth.
'''

tristam = '''
Chapter 2.LXIII.

--Can you tell me, quoth Phutatorius, speaking to Gastripheres who
sat next to him--for one would not apply to a surgeon in so foolish
an affair--can you tell me, Gastripheres, what is best to take out the
fire?--Ask Eugenius, said Gastripheres.--That greatly depends, said
Eugenius, pretending ignorance of the adventure, upon the nature of the
part--If it is a tender part, and a part which can conveniently be wrapt
up--It is both the one and the other, replied Phutatorius, laying his
hand as he spoke, with an emphatical nod of his head, upon the part
in question, and lifting up his right leg at the same time to ease and
ventilate it.--If that is the case, said Eugenius, I would advise you,
Phutatorius, not to tamper with it by any means; but if you will send to
the next printer, and trust your cure to such a simple thing as a soft
sheet of paper just come off the press--you need do nothing more than
twist it round.--The damp paper, quoth Yorick (who sat next to his
friend Eugenius) though I know it has a refreshing coolness in it--yet
I presume is no more than the vehicle--and that the oil and
lamp-black with which the paper is so strongly impregnated, does the
business.--Right, said Eugenius, and is, of any outward application I
would venture to recommend, the most anodyne and safe.

Was it my case, said Gastripheres, as the main thing is the oil and
lamp-black, I should spread them thick upon a rag, and clap it on
directly.--That would make a very devil of it, replied Yorick.--And
besides, added Eugenius, it would not answer the intention, which is
the extreme neatness and elegance of the prescription, which the Faculty
hold to be half in half;--for consider, if the type is a very small one
(which it should be) the sanative particles, which come into contact in
this form, have the advantage of being spread so infinitely thin, and
with such a mathematical equality (fresh paragraphs and large capitals
excepted) as no art or management of the spatula can come up to.--It
falls out very luckily, replied Phutatorius, that the second edition
of my treatise de Concubinis retinendis is at this instant in
the press.--You may take any leaf of it, said Eugenius--no matter
which.--Provided, quoth Yorick, there is no bawdry in it.--

They are just now, replied Phutatorius, printing off the ninth
chapter--which is the last chapter but one in the book.--Pray what
is the title of that chapter? said Yorick; making a respectful bow to
Phutatorius as he spoke.--I think, answered Phutatorius, 'tis that de re
concubinaria.

For Heaven's sake keep out of that chapter, quoth Yorick.

--By all means--added Eugenius.
'''
