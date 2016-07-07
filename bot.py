import Arduino
import telepot
import traceback

ACTIVE_LED = b'1'
DEACTIVE_LED = b'0'
TEMP = b'temp'

class TelegramBot(telepot.Bot):
    
    def __init__(self, token):
        super(TelegramBot, self).__init__(token)
        self.serial = Arduino.start_communication()

    def handle_message(self, msg):
        if 'text' not in msg:
            return
        
        if msg['text'].startswith('/'):
            userName = msg['from']['first_name']+" "+ msg['from']['last_name']
            print('Novo Comando Recebido: ' + msg['text'])
            print('Recebido de: ' + userName)
            self.handle_command(msg)


    def handle_ligarLed(self, msg):
        self.sendMessage(msg['chat']['id'], "Ligando Led")
        
        self.serial.write(ACTIVE_LED)

        response = self.serial.readline()

        if not response:
            response = 'Nenhum dado recebido'
        else:
            response = 'Arduino: ' + response.decode('utf-8')
        
        self.sendMessage(msg['chat']['id'], response)

    def handle_desligarLed(self, msg):
        self.sendMessage(msg['chat']['id'], "Desligando Led")
        
        self.serial.write(DEACTIVE_LED)

        response = self.serial.readline()

        if not response:
            response = 'Nenhum dado recebido'
        else:
            response = response.decode('utf-8')
        
        self.sendMessage(msg['chat']['id'], response)

    def handle_temp(self, msg):
        self.sendMessage(msg['chat']['id'], "Lendo informações do sensor DHT11...")

        self.serial.write(TEMP)
        
        response = self.serial.readline()
        
        if not response:
            response = "Nenhum dado recebido"
       	    self.sendMessage(msg['chat']['id'], response)
        else:
            data = response.decode('utf-8')
            data = data.rstrip('\n')
            data = data.split(';')
            
        self.sendMessage(msg['chat']['id'], 'Temperatura: ' + data[0] + " ºC")        
        self.sendMessage(msg['chat']['id'], 'Umidade: ' + data[1] + ' %')


    def handle_command(self, msg):
        method = 'handle_' + msg['text'][1:]

        if hasattr(self, method):
            getattr(self, method)(msg)

    def runBot(self):
        last_offset = 0
        print('Aguardando Comandos...')

        while True: 
            try:
                updates = self.getUpdates(timeout=60, offset=last_offset)

                if updates:
                    for u in updates:
                        if 'message' in u:
                            self.handle_message(u['message'])

                    last_offset = updates[-1]['update_id'] + 1
                
            except KeyboardInterrupt:
                break
            except:
                traceback.print_exc()
bot = TelegramBot('{TELEGRAM_BOT_API_KEY}')
bot.runBot()