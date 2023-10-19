import re
import datetime

IGNORE_MESSAGES = ['<Media Omitted>','<Multimedia omitido>', 'null']
DATE_PATTERN = r'(?P<date>\d{1,2}/\d{1,2}/\d{2,4}), (?P<time>\d{1,2}:\d{2})'
AUTHOR_PATTERN = r'- (?P<author>.*?):'
CONTENT_PATTERN = r'- .*?: (?P<content>.*)'

def parse_whatsapp_conversation(conversation):
    if isinstance(conversation, str):
        conversation = conversation.split('\n')

    messages = []
    buffer = []
    format_type = infer_date_format(conversation)

    for line in conversation:
        match = re.match(DATE_PATTERN, line)
        if match:
            if buffer:
                parsed_message = parse_message(''.join(buffer), format_type)
                if parsed_message['content']:
                    messages.append(parsed_message)
                buffer = []
        buffer.append(line)

    if buffer:
        parsed_message = parse_message(''.join(buffer), format_type)
        if parsed_message['content']:
            messages.append(parsed_message)
    return messages

def parse_whatsapp_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return parse_whatsapp_conversation(lines)

def parse_message(message, format_type):
    date_match = re.search(DATE_PATTERN, message)
    author_match = re.search(AUTHOR_PATTERN, message)
    content_match = re.search(CONTENT_PATTERN, message)

    content = content_match.group('content').strip() if content_match else None
    for phrase in IGNORE_MESSAGES:
        content = re.sub(re.escape(phrase), "", content, flags=re.IGNORECASE)

    normalized_date = normalize_date_format(date_match.group('date'), format_type) if date_match else None
    time_string = date_match.group('time') if date_match else None
    if time_string:
        hour, minute = time_string.split(':')
        time_string = f"{int(hour):02d}:{int(minute):02d}"

    return {
        'timestamp': f"{normalized_date} {time_string}" if normalized_date and time_string else None,
        'author': author_match.group('author') if author_match else None,
        'content': content
    }

def normalize_date_format(date_string, format_type):
    if format_type == 'DMY':
        date_format = '%d/%m/%y'
    else:
        date_format = '%m/%d/%y'
    date_obj = datetime.datetime.strptime(date_string, date_format)
    return date_obj.strftime('%d/%m/%y')

def infer_date_format(conversation):
    day_first_count = 0
    month_first_count = 0

    for line in conversation:
        match = re.match(DATE_PATTERN, line)
        if match:
            date_parts = match.group('date').split('/')
            if int(date_parts[0]) > 12:
                day_first_count += 1
            else:
                month_first_count += 1

    return 'DMY' if day_first_count > month_first_count else 'MDY'
