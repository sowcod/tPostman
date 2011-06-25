#!/bin/sh

#rsync -progress -Razvv --delete --force --exclude-from='/Users/sohei/Documents/Projects/tpostman/exclude' -e 'ssh -i /Users/sohei/sowcod/key_admin' ./ sowcod.net:/var/www/html/tpostman/ 
rsync -progress -Razvv --delete --force --exclude-from='exclude' -e 'ssh -i /Users/sohei/sowcod/key_admin' ./ sowcod.net:/var/www/html/tpostman/ 
