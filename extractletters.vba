Function ExtractLetters(inputString As String) As String
    Dim i As Integer
    Dim resultString As String
    
    For i = 1 To Len(inputString)
        If IsLetter(Mid(inputString, i, 1)) Then
            resultString = resultString & Mid(inputString, i, 1)
        End If
    Next i
    
    ExtractLetters = resultString
End Function

Function IsLetter(character As String) As Boolean
    IsLetter = character Like "[A-Za-z]"
End Function
