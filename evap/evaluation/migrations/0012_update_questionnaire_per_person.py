# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for q in orm['evaluation.Questionnaire'].objects.all():
            if q.name_de.startswith(u"[A] ") and q.name_en.startswith(u"[A] "):
                q.is_for_persons = False
                q.name_de = q.name_de[4:]
                q.name_en = q.name_en[4:]
            elif q.name_de.startswith(u"[B] ") and q.name_en.startswith(u"[B] "):
                q.is_for_persons = True
                q.name_de = q.name_de[4:]
                q.name_en = q.name_en[4:]
            else:
                # use existing data, majority wins
                with_person = q.assigned_to.filter(lecturer=None).count()
                without_person = q.assigned_to.exclude(lecturer=None).count()
                q.is_for_persons = with_person > without_person
    
    def backwards(self, orm):
        "Write your backwards methods here."
        for q in orm['evaluation.Questionnaire'].objects.all():
            if not q.is_for_persons:
                q.name_de = u"[A] " + q.name_de
                q.name_en = u"[A] " + q.name_en
            else:
                q.name_de = u"[B] " + q.name_de
                q.name_en = u"[B] " + q.name_en

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'evaluation.assignment': {
            'Meta': {'unique_together': "(('course', 'lecturer'),)", 'object_name': 'Assignment'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['evaluation.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecturer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lecturers'", 'null': 'True', 'to': "orm['auth.User']"}),
            'questionnaires': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'assigned_to'", 'blank': 'True', 'to': "orm['evaluation.Questionnaire']"}),
            'read_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'evaluation.course': {
            'Meta': {'ordering': "('semester', 'study', 'name_de')", 'unique_together': "(('semester', 'study', 'name_de'), ('semester', 'study', 'name_en'))", 'object_name': 'Course'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'participant_count': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['evaluation.Semester']"}),
            'state': ('django_fsm.db.fields.fsmfield.FSMField', [], {'default': "'new'", 'max_length': '50'}),
            'study': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'vote_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'vote_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'voter_count': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'voters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'evaluation.gradeanswer': {
            'Meta': {'object_name': 'GradeAnswer'},
            'answer': ('django.db.models.fields.IntegerField', [], {}),
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['evaluation.Assignment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['evaluation.Question']"})
        },
        'evaluation.question': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Question'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['evaluation.Questionnaire']"}),
            'text_de': ('django.db.models.fields.TextField', [], {}),
            'text_en': ('django.db.models.fields.TextField', [], {})
        },
        'evaluation.questionnaire': {
            'Meta': {'ordering': "('obsolete', 'name_de')", 'object_name': 'Questionnaire'},
            'description_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_for_persons': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name_de': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'obsolete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'public_name_de': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'public_name_en': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'teaser_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'teaser_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'evaluation.semester': {
            'Meta': {'ordering': "('-created_at', 'name_de')", 'object_name': 'Semester'},
            'created_at': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'evaluation.textanswer': {
            'Meta': {'object_name': 'TextAnswer'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['evaluation.Assignment']"}),
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['evaluation.Question']"}),
            'reviewed_answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'evaluation.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_lecturer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logon_key': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'logon_key_valid_until': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'proxies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'proxied_users'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['evaluation']
