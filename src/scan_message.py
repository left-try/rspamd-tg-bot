from telegram import Update
from telegram.ext import CallbackContext
import subprocess


def extract_spam_header(result_string):
    lines = result_string.splitlines()
    for line in lines:
        if line.startswith("Spam:"):
            spam_value = line.split(":", 1)[1].strip()
            return spam_value.lower() == "true"
    return None

async def check_message(update: Update, context: CallbackContext):
    message = parse_message(update, context)
    filename = '../message.eml'
    with open(filename, 'w') as file:
        file.write(message)
    command = ['rspamc', filename]
    result = subprocess.run(command, capture_output=True, text=True)
    return False

def parse_message(update: Update, context: CallbackContext):
    message_text = update.message.text
    reply_message = update.message.reply_to_message
    message = f"""
Return-Path: <cfrg-bounces@irtf.org>
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/simple; d=ietf.org; s=ietf1;
	t=1557262917; bh=u0s27csbY4DoorjT0i6xdMU7DX5zBvyJdaTBxev7WE8=;
	h=To:References:From:Date:In-Reply-To:Subject:List-Id:
	 List-Unsubscribe:List-Archive:List-Post:List-Help:List-Subscribe:
	 Cc;
	b=D8Kty+gIkEInNAFcwmrAdpVfIHfzKGAKQrSgQyhT4khKxq7jZFOX5gaNw0pWD/rUB
	 Sdumgfb+/iFZgG+M/xn8B7ANFNkQO65cWvVmYQ6TQxXE4uhFmehPzzDIWtlsizKnLf
	 ItaQ2K4huFk+5FSyGuc56PqZtZa4S/Mkz3kX0w5E=
X-Mailbox-Line: From cfrg-bounces@irtf.org  Tue May  7 14:01:51 2019
Received: from ietfa.amsl.com (localhost [IPv6:::1])
	by ietfa.amsl.com (Postfix) with ESMTP id 8569D12025D;
	Tue,  7 May 2019 14:01:16 -0700 (PDT)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/simple; d=ietf.org; s=ietf1;
	t=1557262877; bh=u0s27csbY4DoorjT0i6xdMU7DX5zBvyJdaTBxev7WE8=;
	h=To:References:From:Date:In-Reply-To:Subject:List-Id:
	 List-Unsubscribe:List-Archive:List-Post:List-Help:List-Subscribe:
	 Cc;
	b=jjHHLfvBzn3yzgYs0e1ROi1mK3zyHxZX4rrkkloh/EdQuG0R59ablyQk++nkgqPe4
	 URZxEYII4EjhJTRM5r/mbpdBvZ5lG9IQv7faR3jSmFRtTjJhOTR9sr09dMW3GENtYE
	 P0+NBPR1vU+czz/4XSvbPM1nj4oYLJ/Qe2FTFhEE=
X-Original-To: cfrg@ietfa.amsl.com
Delivered-To: cfrg@ietfa.amsl.com
Received: from localhost (localhost [127.0.0.1])
 by ietfa.amsl.com (Postfix) with ESMTP id 00E7712024B
 for <cfrg@ietfa.amsl.com>; Tue,  7 May 2019 14:01:07 -0700 (PDT)
Received: from mail.ietf.org ([4.31.198.44])
 by localhost (ietfa.amsl.com [127.0.0.1]) (amavisd-new, port 10024)
 with ESMTP id k8UsBTUjeiTe for <cfrg@ietfa.amsl.com>;
 Tue,  7 May 2019 14:01:04 -0700 (PDT)
 From: {update.effective_user.username}@example.com
 """ + (f"To: {update.effective_chat.username}@example.com" if reply_message is None
                      else f"Reply-to:{reply_message.from_user.username}@example.com") + f"""
Message-ID: <0a67411b-9a2d-9e08-ca06-08ea938c0c89@gmail.com>
Date: Tue, 7 May 2019 17:01:00 -0400
MIME-Version: 1.0
Subject: Re: [Cfrg] Adoption call for draft-sullivan-cfrg-voprf
Precedence: list
List-Id: Crypto Forum Research Group <cfrg.irtf.org>
List-Unsubscribe: <https://www.irtf.org/mailman/options/cfrg>,
 <mailto:cfrg-request@irtf.org?subject=unsubscribe>
List-Archive: <https://mailarchive.ietf.org/arch/browse/cfrg/>
List-Post: <mailto:cfrg@irtf.org>
List-Help: <mailto:cfrg-request@irtf.org?subject=help>
List-Subscribe: <https://www.irtf.org/mailman/listinfo/cfrg>,
 <mailto:cfrg-request@irtf.org?subject=subscribe>
Cc: "draft-sullivan-cfrg-voprf.authors@ietf.org"
 <draft-sullivan-cfrg-voprf.authors@ietf.org>
Content-Type: multipart/mixed; boundary="===============0339907768802969961=="
Errors-To: cfrg-bounces@irtf.org
Sender: "Cfrg" <cfrg-bounces@irtf.org>
Content-Type: text/plain; charset=utf-8; format=flowed
{message_text}
"""
    return message

