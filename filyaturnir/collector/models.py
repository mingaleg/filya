from django.db import models
from os import path, system
import subprocess
from django.contrib.auth.models import User
from django.db.models import Q
from random import shuffle
import threading


SOURCE_FILES_DIR = '/root/filya/submits/source/'
EXEC_FILES_DIR = '/root/filya/submits/bin/'
SANDBOX_DIR = '/root/filya/submits/sandbox/'
SANDBOX_COMPILER = '/root/filya/submits/compile.py'
FINAL_DIR = '/root/filya/submits/final/'

INTERACTOR = '/root/filya/filyaturnir/collector/interaction/interactor.py'
JSLOG_DIR = '/root/filya/battles/js'
TXTLOG_DIR = '/root/filya/battles/txt'


EXTENTIONS = {
    'py3': '.py',
    'fpc': '.pas',
    'g++': '.cpp',
}

def get_lasts_ok_submits():
    submits = []
    for user in User.objects.filter(is_staff=False):
        foo = Submit.objects.filter(user=user, status="OK", current=True)
        if foo:
            submits.append(foo[0])
    return submits

class Submit(models.Model):
    sid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)
    current = models.BooleanField(default=False)
    source = models.TextField()
    LANGUAGE_CHOICES = (
        #('py2', 'python2'),
        ('py3', 'python3'),
        ('fpc', 'fpc'),
        ('g++', 'g++'),
    )
    language = models.CharField(max_length=3, default='', choices=LANGUAGE_CHOICES)
    source_file = models.CharField(max_length=255, default="", blank=True)
    exec_file = models.CharField(max_length=255, default="", blank=True)
    log = models.TextField(blank=True)
    check_battle = models.ForeignKey('Battle', blank=True, null=True)
    STATUS_CHOICES = (
        ('PD', 'Pending'),
        ('OK', 'OK'),
        ('RU', 'Running'),
        ('CE', 'Compilation Error'),
        ('FA', 'Failed'),
        ('PE', 'Presentation Error'),
        ('TL', 'Time Limit'),
        ('RE', 'Runtime Error'),
        ('CR', 'Compiling'),
    )
    status = models.CharField(max_length=2, default="PD", choices=STATUS_CHOICES)

#    def submit(self):
#        t = threading.Thread(target=self._submit, args=[])
#        t.setDaemon(True)
#        t.start()

    def submit(self):
        self.logs = ''
        self.source_file = path.join(SOURCE_FILES_DIR, self.user.username + '.' + str(self.sid) + EXTENTIONS[self.language])
        with open(self.source_file, 'w') as fh:
            fh.write(self.source)
        self.status = 'PD'
        self.save()
        self.compile_source()

    def reset(self):
        self.logs = ''
        self.status = 'PD'
        self.exec_file = ''
        self.current = False
        self.save()

    def compile_source(self):
        try:
            self.status = 'CR'
            self.save()
            sandfilename = path.join(SANDBOX_DIR, path.split(self.source_file)[1])
            resultname = path.join(EXEC_FILES_DIR, path.splitext(path.split(sandfilename)[1])[0])
            system('cp %s %s' % (self.source_file, sandfilename))
            failed = False
            try:
                log = subprocess.check_output([SANDBOX_COMPILER, sandfilename, resultname], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as E:
                failed = True
                log = E.output
            self.log = log
            if failed:
                self.status = 'CE'
                self.save()
                return
            binname = path.join(EXEC_FILES_DIR, path.splitext(path.split(sandfilename)[1])[0])
            self.exec_file = binname
            self.status = 'RU'
            self.save()
            self.run()
        except Exception as E:
            self.log = 'Server fail: please contact the administrator\n' + str(E)
            self.status = 'FA'
            self.save()

    def make_current(self):
        foo = list(Submit.objects.filter(user=self.user, status="OK").order_by('sid').all())
        for bar in foo[:-1]:
            bar.current = False
            bar.save()
        foo[-1].current = True
        foo[-1].save()

    def run(self):
        self.status = 'RU'
        battle = Battle(player1=self, player2=self)
        battle.save()
        self.check_battle = battle
        battle.run(True)
        if battle.status == 'IG':
            self.status = 'FA'
        else:
            self.status = battle.status
        self.save()
        if self.status == 'OK':
            self.make_current()

    def __str__(self):
        return self.user.username + '[' + str(self.sid) + ']'

class Battle(models.Model):
    player1 = models.ForeignKey(Submit, related_name="played1")
    player2 = models.ForeignKey(Submit, related_name="played2")
    score = models.CharField(max_length=200, default='?-?')
    done = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now=True)
    sid = models.AutoField(primary_key=True)
    comment = models.TextField(blank=True, null=True)
    winner = models.ForeignKey(Submit, null=True, blank=True, related_name="wins")
    serial = models.ForeignKey('BattleSerial', blank=True, null=True, default=None)
    STATUS_CHOICES = (
        ('OK', 'OK'),
        ('PE', 'Presentation Error'),
        ('TL', 'Time Limit'),
        ('RE', 'Runtime Error'),
        ('RU', 'Running'),
        ('FA', 'Failed'),
        ('IG', 'Ignored'),
        ('PD', 'Pending'),
    )
    status = models.CharField(max_length=2, default='PD', choices=STATUS_CHOICES)

#    def run(self, running=False):
#        t = threading.Thread(target=self._run, args=[running])
#        t.setDaemon(True)
 #       t.start()

    def run(self, running=False):
        self.status = 'RU'
        self.save()
        if running:
            if self.player1.status != 'RU' or self.player2.status != 'RU':
                self.done = True
                self.comment = "Expected runnings"
                self.status = 'IG'
                self.save()
                return
        else:
            if self.player1.status != 'OK' or self.player2.status != 'OK':
                self.done = True
                self.comment = "Not OK submissions"
                self.status = 'IG'
                self.save()
                return
        p = subprocess.Popen([INTERACTOR, self.player1.exec_file, self.player2.exec_file], 
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        stdout, stderr = stdout.decode(), stderr.decode()
        if p.returncode:
            self.comment = "Interaction error"
            self.status = 'FA'
            self.done = True
            self.save()
            return
        with open(path.join(JSLOG_DIR, str(self.sid)+'.js'), 'w') as fh:
            fh.write(stdout)
        with open(path.join(TXTLOG_DIR, str(self.sid)+'.txt'), 'w') as fh:
            fh.write(stderr)
        log = eval(stdout.split('=')[1].strip())
        pw = log['winner']
        if pw == 1:
            self.winner = self.player1
        elif pw == 2:
            self.winner = self.player2
        else:
            self.comment = "Wrong player wins"
            self.done = True
            self.status = 'FA'
            self.save()
            return

        st, move, score = log['log'][-1]
        if st == 'OK':
            self.score = '%d-%d'%(score[0], score[1])
            self.status = 'OK'
        else:
            self.score = 'FAULT'
            self.status = st
        self.done = True
        self.success = True
        self.save()
    def __str__(self):
        return "[%d] %s vs %s: %s" % (self.sid, str(self.player1), str(self.player2), self.score)
    def player1status(self):
        if not self.winner:
            return 'unknown'
        if self.player1 == self.winner:
            return 'winner'
        else:
            return 'looser'
    def player2status(self):
        if not self.winner:
            return 'unknown'
        if self.player2 == self.winner:
            return 'winner'
        else:
            return 'looser'

from django.core.exceptions import ValidationError
def validate_odd(value):
    if value % 2 != 1:
        raise ValidationError('%s is not an odd number' % value)

class BattleSerial(models.Model):
    sid = models.AutoField(primary_key=True)
    player1 = models.ForeignKey(Submit, related_name="serplayed1")
    player2 = models.ForeignKey(Submit, related_name="serplayed2")
    games = models.IntegerField(default=3, validators=[validate_odd])
    played = models.IntegerField(default=0)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    winner = models.ForeignKey(Submit, blank=True, null=True)
    failed = models.BooleanField(default=False)
#    started = models.BooleanField(default=False)
    
#    def run(self):
#        t = threading.Thread(target=self._run, args=[])
#        t.setDaemon(True)
#        t.start()

    def run(self):
#        self.started = True
        self.save()
        self.battle_set.clear()
        self.played = 0
        self.score1 = 0
        self.score2 = 0
        self.winner = None
        self.failed = False
        p = [self.player1, self.player2]
        shuffle(p)
        p1, p2 = p
        for i in range(self.games):
            battle = Battle(player1=p1, player2=p2, serial=self)
            battle.save()
            battle.run()
            if battle.status in ('FA', 'IG'):
                self.failed = True
                self.save()
                return
            self.played += 1
            if battle.winner == self.player1:
                self.score1 += 1
            else:
                self.score2 += 1
            stop = False
            if self.score1 * 2 > self.games:
                self.winner = self.player1
                stop = True
            if self.score2 * 2 > self.games:
                self.winner = self.player2
                stop = True
            self.save()
            if stop:
                break
            p1, p2 = p2, p1
    def __str__(self):
        return "[%d] %s vs %s: %d-%d (bo %d)" % (self.sid,
                                                 self.player1, self.player2,
                                                 self.score1, self.score2,
                                                 self.games)
    def battles(self):
        return Battle.objects.filter(serial=self).order_by('sid')
    def player1status(self):
        if not self.winner:
            return 'unknown'
        if self.player1 == self.winner:
            return 'winner'
        else:
            return 'looser'
    def player2status(self):
        if not self.winner:
            return 'unknown'
        if self.player2 == self.winner:
            return 'winner'
        else:
            return 'looser'
