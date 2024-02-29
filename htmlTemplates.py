css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #F7F7F7
}
.chat-message.bot {
    background-color: #F7F7F7
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #000000;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="images/little_ai_bites_logo.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="images/little_ai_bites_logo.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
