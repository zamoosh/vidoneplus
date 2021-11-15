from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import re
from django.core.validators import validate_email
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.http.response import HttpResponseRedirect
import datetime
from client.models import Setting as usetting, Status

from django.contrib.auth import get_user_model

User = get_user_model()


def error_handler(lang, status, exist):
    if lang and lang == 'en':
        if status == 200:
            return {'msg': 'Operation successfully done.'}
        elif status == 429:
            return {'msg': 'Operation successfully done with some limits because of your package type.'}
        elif status == 400:
            return {'msg': 'Operation failed because of your package type.'}
        elif exist and exist is True:
            return {'msg': 'This item exist'}
        else:
            return {'msg': 'Operation failed.'}

    else:
        if status == 200:
            return {'msg': 'عملیات با موفقیت انجام شد'}
        elif status == 429:
            return {'msg': 'عملیات به علت محدودیت بسته خریداری شده شما با محدودیت انجام شد'}
        elif status == 400:
            return {'msg': 'پکیج خریداری شده توسط شما امکان انجام این فعالیت را ندارد'}
        elif exist and exist is True:
            return {'msg': 'این آیتم از قبل ذخیره گردیده است'}
        else:
            return {'msg': 'در انجام عملیات خطایی رخ داده است'}


def findSeqChar(CharLocs, src):
    AllSeqChars = []
    i = 0
    SeqChars = []
    while i < len(CharLocs) - 1:
        if CharLocs[i + 1] - CharLocs[i] == 1 and \
                ord(src[CharLocs[i + 1]]) - ord(src[CharLocs[i]]) == 1:
            # We find a pair of sequential chars!
            if not SeqChars:
                SeqChars = [src[CharLocs[i]], src[CharLocs[i + 1]]]
            else:
                SeqChars.append(src[CharLocs[i + 1]])
        else:
            if SeqChars:
                AllSeqChars.append(SeqChars)
                SeqChars = []
        i += 1
    if SeqChars:
        AllSeqChars.append(SeqChars)
    return AllSeqChars


def pwStrength(pw):
    Score = 0
    Length = len(pw)
    Score += Length * 4
    NUpper = 0
    NLower = 0
    NNum = 0
    NSymbol = 0
    LocUpper = []
    LocLower = []
    LocNum = []
    LocSymbol = []
    CharDict = {}
    for i in range(Length):
        Ch = pw[i]
        Code = ord(Ch)
        if Code >= 48 and Code <= 57:
            NNum += 1
            LocNum.append(i)
        elif Code >= 65 and Code <= 90:
            NUpper += 1
            LocUpper.append(i)
        elif Code >= 97 and Code <= 122:
            NLower += 1
            LocLower.append(i)
        else:
            NSymbol += 1
            LocSymbol.append(i)
        if not Ch in CharDict:
            CharDict[Ch] = 1
        else:
            CharDict[Ch] += 1
    if NUpper != Length and NLower != Length:
        if NUpper != 0:
            Score += (Length - NUpper) * 2
            # print("Upper case score:", (Length - NUpper) * 2)
        if NLower != 0:
            Score += (Length - NLower) * 2
            # print("Lower case score:", (Length - NLower) * 2)
    if NNum != Length:
        Score += NNum * 4
        # print("Number score:", NNum * 4)
    Score += NSymbol * 6
    # print("Symbol score:", NSymbol * 6)
    # Middle number or symbol
    Score += len([i for i in LocNum if i != 0 and i != Length - 1]) * 2
    # print("Middle number score:", len([i for i in LocNum if i != 0 and i != Length - 1]) * 2)
    Score += len([i for i in LocSymbol if i != 0 and i != Length - 1]) * 2
    # print("Middle symbol score:", len([i for i in LocSymbol if i != 0 and i != Length - 1]) * 2)
    # Letters only?
    if NUpper + NLower == Length:
        Score -= Length
        # print("Letter only:", -Length)
    if NNum == Length:
        Score -= Length
        # print("Number only:", -Length)
    # Repeating chars
    Repeats = 0
    for Ch in CharDict:
        if CharDict[Ch] > 1:
            Repeats += CharDict[Ch] - 1
    if Repeats > 0:
        Score -= int(Repeats / (Length - Repeats)) + 1
        # print("Repeating chars:", -int(Repeats / (Length - Repeats)) - 1)
    if Length > 2:
        # Consequtive letters
        for MultiLowers in re.findall(''.join(["[a-z]{2,", str(Length), '}']), pw):
            Score -= (len(MultiLowers) - 1) * 2
            # print("Consequtive lowers:", -(len(MultiLowers) - 1) * 2)
        for MultiUppers in re.findall(''.join(["[A-Z]{2,", str(Length), '}']), pw):
            Score -= (len(MultiUppers) - 1) * 2
            # print("Consequtive uppers:", -(len(MultiUppers) - 1) * 2)
        # Consequtive numbers
        for MultiNums in re.findall(''.join(["[0-9]{2,", str(Length), '}']), pw):
            Score -= (len(MultiNums) - 1) * 2
            # print("Consequtive numbers:", -(len(MultiNums) - 1) * 2)
        # Sequential letters
        LocLetters = (LocUpper + LocLower)
        LocLetters.sort()
        for Seq in findSeqChar(LocLetters, pw.lower()):
            if len(Seq) > 2:
                Score -= (len(Seq) - 2) * 2
                # print("Sequential letters:", -(len(Seq) - 2) * 2)
        # Sequential numbers
        for Seq in findSeqChar(LocNum, pw.lower()):
            if len(Seq) > 2:
                Score -= (len(Seq) - 2) * 2
                # print("Sequential numbers:", -(len(Seq) - 2) * 2)
    return Score
