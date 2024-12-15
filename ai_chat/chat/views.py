from django.shortcuts import render, redirect
import markdown
from django.utils.safestring import mark_safe
from .api.ai import AIService

def index(request):
    if not 'chat_history' in request.session:
        request.session['chat_history'] = []
    
    if request.method == 'POST':
        if 'clear_chat' in request.POST:
            request.session['chat_history'] = []
            request.session.modified = True
            return redirect('index')
            
        user_message = request.POST.get('message', '').strip()
        if user_message:
            # Add user message to history
            request.session['chat_history'].append({
                'role': 'user',
                'content': user_message
            })
            
            # Get AI response
            ai_service = AIService()
            ai_response = ai_service.get_chat_response(request.session['chat_history'])
            
            # Convert markdown to HTML with extensions
            html_content = markdown.markdown(
                ai_response,
                extensions=[
                    'fenced_code',
                    'codehilite',
                    'tables',
                    'nl2br'
                ]
            )
            
            # Add AI response to history
            request.session['chat_history'].append({
                'role': 'assistant',
                'content': mark_safe(html_content)
            })
            
            request.session.modified = True
    
    # Process any existing messages in chat history
    processed_history = []
    for message in request.session.get('chat_history', []):
        if message['role'] == 'assistant':
            # Re-process markdown for assistant messages
            html_content = markdown.markdown(
                message['content'] if isinstance(message['content'], str) else str(message['content']),
                extensions=[
                    'fenced_code',
                    'codehilite',
                    'tables',
                    'nl2br'
                ]
            )
            processed_history.append({
                'role': 'assistant',
                'content': mark_safe(html_content)
            })
        else:
            processed_history.append(message)
    
    return render(request, 'chat/index.html', {
        'chat_history': processed_history
    })