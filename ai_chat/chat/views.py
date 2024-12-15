from django.shortcuts import render, redirect
from .api.ai import AIService
import markdown
from django.utils.safestring import mark_safe
import os
from datetime import datetime

def index(request):
    if not 'chat_history' in request.session:
        request.session['chat_history'] = []
    
    if request.method == 'POST':
        # Check if this is a clear chat request
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
            
            # Save the session
            request.session.modified = True
    
    return render(request, 'chat/index.html', {
        'chat_history': request.session.get('chat_history', [])
    })