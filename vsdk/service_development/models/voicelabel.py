from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe


from .validators import validate_audio_file_extension, validate_audio_file_format

from number_generator.program import *


class VoiceLabel(models.Model):
    name = models.CharField(_('Name'),max_length=50)
    description = models.CharField(_('Description'),max_length=1000, blank = True, null = True)

    class Meta:
        verbose_name = _('Voice Label')

    def __str__(self):
        return _("Voice Label") + ": %s" % (self.name)

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self, language):
        errors = []        
        if len(self.voicefragment_set.filter(language = language)) > 0:
            errors.extend(self.voicefragment_set.filter(language=language)[0].validator())
        else:
            errors.append(ugettext('"%(description_of_this_element)s" does not have a Voice Fragment for "%(language)s"') %{'description_of_this_element' : str(self),'language' : str(language)})
        return errors

    def get_voice_fragment_url(self, language):
        result = self.voicefragment_set.filter(language=language)
        if result: return result[0].get_url()
        else: return ''

class Language(models.Model):
    name = models.CharField(_('Name'),max_length=100, unique = True)
    code = models.CharField(_('Code'),max_length=10, unique = True)
    voice_label = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = _('Language voice label'),
            related_name = 'language_description_voice_label',
            help_text = _("A Voice Label of the name of the language"))
    error_message = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = _('Error message voice label'),
            related_name = 'language_error_message',
            help_text = _("A general error message"))
    select_language = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = _('Select language voice label'),
            related_name = 'language_select_language',
            help_text = _("A message requesting the user to select a language"))
    pre_choice_option = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = _('Pre-Choice Option voice label'),
            related_name = 'language_pre_choice_option',
            help_text = _("The fragment that is to be played before a choice option (e.g. '[to select] option X, please press 1')"))
    post_choice_option = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = _('Post-Choice Option voice label'),
            related_name = 'language_post_choice_option',
            help_text = _("The fragment that is to be played before a choice option (e.g. 'to select option X, [please press] 1')"))
    zero = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'0'},
            related_name = 'language_zero',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'0'})
    one = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'1'},
            related_name = 'language_one',
            help_text = ugettext('The number %(number)s (for en,fr,bm)')% {'number':'1'})
    two = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'2'},
            related_name = 'language_two',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'2'})
    three = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'3'},
            related_name = 'language_three',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'3'})
    four = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'4'},
            related_name = 'language_four',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'4'})
    five = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'5'},
            related_name = 'language_five',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'5'})
    six = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'6'},
            related_name = 'language_six',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'6'})
    seven = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'7'},
            related_name = 'language_seven',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'7'})
    eight = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'8'},
            related_name = 'language_eight',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'8'})
    nine = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'9'},
            related_name = 'language_nine',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'9'})
    ten = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'10'},
            related_name = 'language_ten',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'10'})
    eleven = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'11'},
            related_name = 'language_eleven',
            help_text = ugettext("The number %(number)s (for en,fr)")% {'number':'11'})
    twelve = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'12'},
            related_name = 'language_twelve',
            help_text = ugettext("The number %(number)s (for en,fr)")% {'number':'12'})
    thirteen = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'13'},
            related_name = 'language_thirteen',
            help_text = ugettext("The number %(number)s (for en,fr)")% {'number':'13'})
    fourteen = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'14'},
            related_name = 'language_fourteen',
            help_text = ugettext("The number %(number)s (for en,fr)")% {'number':'14'})
    fifteen = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'15'},
            related_name = 'language_fifteen',
            help_text = ugettext("The number %(number)s (for en,fr)")% {'number':'15'})
    sixteen = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'16'},
            related_name = 'language_sixteen',
            help_text = ugettext("The number %(number)s (for en,fr)")% {'number':'16'})
    seventeen = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'17'},
            related_name = 'language_seventeen',
            help_text = ugettext("The number %(number)s (for en)")% {'number':'17'})
    eighteen = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'18'},
            related_name = 'language_eighteen',
            help_text = ugettext("The number %(number)s (for en)")% {'number':'18'})
    nineteen = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'19'},
            related_name = 'language_nineteen',
            help_text = ugettext("The number %(number)s (for en)")% {'number':'19'})
    twenty = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'20'},
            related_name = 'language_twenty',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'20'})
    thirty = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'30'},
            related_name = 'language_thirty',
            help_text = ugettext("The number %(number)s (for en,fr)")% {'number':'30'})
    fourty = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'40'},
            related_name = 'language_fourty',
            help_text = ugettext("The number %(number)s (for en,fr)")% {'number':'40'})
    fifty = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'50'},
            related_name = 'language_fifty',
            help_text = ugettext("The number %(number)s (for en,fr)")% {'number':'50'})
    sixty = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'60'},
            related_name = 'language_sixty',
            help_text = ugettext("The number %(number)s (for en,fr)")% {'number':'60'})
    seventy = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'70'},
            related_name = 'language_seventy',
            help_text = ugettext("The number %(number)s (for en)")% {'number':'70'})
    eighty = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'80'},
            related_name = 'language_eighty',
            help_text = ugettext("The number %(number)s (for en,fr)")% {'number':'80'})
    ninety = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'90'},
            related_name = 'language_ninety',
            help_text = ugettext("The number %(number)s (for en)")% {'number':'90'})
    hundred = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'100'},
            related_name = 'language_hundred',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'100'})
    thousand = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'1000'},
            related_name = 'language_thousand',
            help_text = ugettext("The number %(number)s (for en,fr,bm)")% {'number':'1000'})
    andsep = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number separator %(number)s")% {'number':'and'},
            related_name = 'language_and',
            help_text = ugettext("The number separator %(number)s (for en,fr,bm)")% {'number':'and'})
    commasep = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number separator %(number)s")% {'number':'comma'},
            related_name = 'language_comma',
            help_text = ugettext("The number separator %(number)s (for en,fr: a small silence)")% {'number':'comma'})
    tens = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number multitude %(number)s")% {'number':'10'},
            related_name = 'language_tens',
            help_text = ugettext("The number multitude %(number)s (for bm)")% {'number':'10'})
    hundreds = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number multitude %(number)s")% {'number':'100'},
            related_name = 'language_hundreds',
            help_text = ugettext("The number multitude %(number)s (for fr,bm)")% {'number':'100'})
    thousands = models.ForeignKey('VoiceLabel', null = True, default = None, blank = True,
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number multitude %(number)s")% {'number':'1000'},
            related_name = 'language_thousands',
            help_text = ugettext("The number multitude %(number)s (for bm)")% {'number':'1000'})

    class Meta:
        verbose_name = _('Language')

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)

    @property
    def get_description_voice_label_url(self):
        """
        Returns the URL of the Voice Fragment describing
        the language, in the language itself.
        """
        return self.voice_label.get_voice_fragment_url(self)

    @property
    def get_interface_numbers_voice_label_url_list(self):
        numbers = [
                    self.zero,
                    self.one,
                    self.two,
                    self.three,
                    self.four,
                    self.five,
                    self.six,
                    self.seven,
                    self.eight,
                    self.nine
                    ]
        result = []
        for number in numbers:
            result.append(number.get_voice_fragment_url(self))
        return result
    
    @property
    def get_interface_numbers_voice_label_url_dict(self):
        result = {}
        if self.zero: result[0] = self.zero.get_voice_fragment_url(self)
        if self.one: result[1] = self.one.get_voice_fragment_url(self)
        if self.two: result[2] = self.two.get_voice_fragment_url(self)
        if self.three: result[3] = self.three.get_voice_fragment_url(self)
        if self.four: result[4] = self.four.get_voice_fragment_url(self)
        if self.five: result[5] = self.five.get_voice_fragment_url(self)
        if self.six: result[6] = self.six.get_voice_fragment_url(self)
        if self.seven: result[7] = self.seven.get_voice_fragment_url(self)
        if self.eight: result[8] = self.eight.get_voice_fragment_url(self)
        if self.nine: result[9] = self.nine.get_voice_fragment_url(self)
        if self.ten: result[10] = self.ten.get_voice_fragment_url(self)
        if self.eleven: result[11] = self.eleven.get_voice_fragment_url(self)
        if self.twelve: result[12] = self.twelve.get_voice_fragment_url(self)
        if self.thirteen: result[13] = self.thirteen.get_voice_fragment_url(self)
        if self.fourteen: result[14] = self.fourteen.get_voice_fragment_url(self)
        if self.fifteen: result[15] = self.fifteen.get_voice_fragment_url(self)
        if self.sixteen: result[16] = self.sixteen.get_voice_fragment_url(self)
        if self.seventeen: result[17] = self.seventeen.get_voice_fragment_url(self)
        if self.eighteen: result[18] = self.eighteen.get_voice_fragment_url(self)
        if self.nineteen: result[19] = self.nineteen.get_voice_fragment_url(self)
        if self.twenty: result[20] = self.twenty.get_voice_fragment_url(self)
        if self.thirty: result[30] = self.thirty.get_voice_fragment_url(self)
        if self.fourty: result[40] = self.fourty.get_voice_fragment_url(self)
        if self.fifty: result[50] = self.fifty.get_voice_fragment_url(self)
        if self.sixty: result[60] = self.sixty.get_voice_fragment_url(self)
        if self.seventy: result[70] = self.seventy.get_voice_fragment_url(self)
        if self.eighty: result[80] = self.eighty.get_voice_fragment_url(self)
        if self.ninety: result[90] = self.ninety.get_voice_fragment_url(self)
        if self.hundred: result[100] = self.hundred.get_voice_fragment_url(self)
        if self.thousand: result[1000] = self.thousand.get_voice_fragment_url(self)
        if self.andsep: result['and'] = self.andsep.get_voice_fragment_url(self)
        if self.commasep: result['comma'] = self.commasep.get_voice_fragment_url(self)
        if self.tens: result['10s'] = self.tens.get_voice_fragment_url(self)
        if self.hundreds: result['100s'] = self.hundreds.get_voice_fragment_url(self)
        if self.thousands: result['1000s'] = self.thousands.get_voice_fragment_url(self)
        return result
    
    def generate_number(self,d):
        code = '%s' % (self.code)
        dict = self.get_interface_numbers_voice_label_url_dict
        if (code == 'en'):
            return generate_num_english(d, dict);
        if (code == 'fr'):
            return generate_numb_french(d, dict);
        if (code == 'bm'):
            return generate_num_bambara(d, dict);
        return []

    @property
    def get_interface_voice_label_url_dict(self):
        """
        Returns a dictionary containing all URLs of Voice
        Fragments of the hardcoded interface audio fragments.
        """
        interface_voice_labels = {
                'voice_label':self.voice_label,
                'error_message':self.error_message,
                'select_language':self.select_language,
                'pre_choice_option':self.pre_choice_option,
                'post_choice_option':self.post_choice_option,
                }
        for k, v in interface_voice_labels.items():
            interface_voice_labels[k] = v.get_voice_fragment_url(self)
        return interface_voice_labels



class VoiceFragment(models.Model):
    parent = models.ForeignKey('VoiceLabel',
            on_delete = models.CASCADE)
    language = models.ForeignKey(
            'Language',
            on_delete = models.CASCADE)
    audio = models.FileField(_('Audio'),
            validators=[validate_audio_file_extension],
            help_text = _("Ensure your file is in the correct format! Wave (.wav) : Sample rate 8KHz, 16 bit, mono, Codec: PCM 16 LE (s16l)"))


    class Meta:
        verbose_name = _('Voice Fragment')

    def convert_wav_to_correct_format(self):
        from vsdk import settings
        if not settings.KASADAKA:
            pass

        import subprocess
        from os.path import basename
        new_file_name = self.audio.path[:-4] + "_conv.wav"
        subprocess.getoutput("sox -S %s -r 8k -b 16 -c 1 -e signed-integer %s"% (self.audio.path, new_file_name))
        self.audio = basename(new_file_name)
        
        


    def save(self, *args, **kwargs):
        super(VoiceFragment, self).save(*args, **kwargs)
        from vsdk import settings
        if  settings.KASADAKA:
            format_correct = validate_audio_file_format(self.audio)
            if not format_correct: 
                self.convert_wav_to_correct_format()
        super(VoiceFragment, self).save(*args, **kwargs)




    def __str__(self):
        return _("Voice Fragment: (%(name)s) %(name_parent)s") % {'name' : self.language.name, 'name_parent' : self.parent.name}

    def get_url(self):
        return self.audio.url

    def validator(self):
        errors = []
        try:
            accessible = self.audio.storage.exists(self.audio.name)
        except NotImplementedError:
            import urllib.request
            try:
                response = urllib.request.urlopen(self.audio.url)
                accessible = True
            except urllib.error.HTTPError:
                accessible = False


        if not self.audio:
            errors.append(ugettext('%s does not have an audio file')%str(self))
        elif not accessible:
            errors.append(ugettext('%s audio file not accessible')%str(self))
        #TODO verift whether this really is not needed anymore
        #elif not validate_audio_file_format(self.audio):
        #    errors.append(ugettext('%s audio file is not in the correct format! Should be: Wave: Sample rate 8KHz, 16 bit, mono, Codec: PCM 16 LE (s16l)'%str(self)))
        return errors

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio:
            file_url = settings.MEDIA_URL + str(self.audio)
            player_string = str('<audio src="%s" controls>'  % (file_url) + ugettext('Your browser does not support the audio element.') + '</audio>')
            return mark_safe(player_string)

    audio_file_player.short_description = _('Audio file player')


