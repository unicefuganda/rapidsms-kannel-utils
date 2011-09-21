#!/usr/bin/env python
from xml.dom import minidom
import urllib2

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from kannel_utils.settings import SMSC_ADMINS,KANNEL_STATUS,RECEPIENTS

def get_status(recepients):
        try:
            response=urllib2.urlopen(KANNEL_STATUS)
        except urllib2.URLError, e:
            if not hasattr(e, "code"):
                raise
            print e
        if response.code==200:
            raw_data=response.read()
            xmldoc = minidom.parseString(raw_data)
            smsc_list=xmldoc.getElementsByTagName('smsc')
            for smsc in smsc_list:
                if smsc.getElementsByTagName('status')[0].childNodes[0].data.split(" ")[0] !="online":
                    smsc_name=smsc.getElementsByTagName('id')[0].childNodes[0].data
                    if smsc_name in SMSC_ADMINS.keys():
                       recepients.join(SMSC_ADMINS.get(smsc_name))
                    subject=smsc_name + " is down!!"
                    message=smsc_name + " is down!! "+\
                    " more info: %s"%KANNEL_STATUS

                    send_mail(subject, message, settings.EMAIL_HOST_USER,
                    recepients, fail_silently=False)
        else:
            subject="Kannel id down"
            send_mail(subject,subject, settings.EMAIL_HOST_USER,
                    recepients, fail_silently=False)


                    
class Command(BaseCommand):
    help = "monitor the kannel smsc links  and send a email notification if one of them is down "
    
    def handle(self, *args, **options):
        get_status(RECEPIENTS)

