import re
emojis = {'😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '🥲', '🥹', '☺️', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🥸', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😮‍💨', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🫣', '🤗', '🫡', '🤔', '🫢', '🤭', '🤫', '🤥', '😶', '😶‍🌫️', '😐', '😑', '😬', '🫨', '🫠', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '😵‍💫', '🫥', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾', '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾'}

def modify_string(input_string):
    # Remove everything that looks like [^3^], [^4^], etc.
    output_string = re.sub(r'\[\^\d+\^\]', '', input_string)
    
    # Remove "Hallo, das ist Bing. "
    output_string = output_string.replace('Hallo, das ist Bing. ', '')
    output_string = output_string.replace('```markdown', '')
    for emoji in emojis:
        output_string = output_string.replace(emoji, '')
    
    return output_string


print(modify_string("""

Hallo, das ist Bing. Ich kann dir helfen, eine Geschichte über ein kleines Mädchen zu erfinden. 😊

Es gibt viele Möglichkeiten, eine solche Geschichte zu schreiben. Du kannst dich von bestehenden Märchen oder Geschichten inspirieren lassen, wie zum Beispiel "Das kleine bucklige Mädchen" [^1^] oder "Die Sterntaler" [^3^]. Oder du kannst deine eigene Fantasie benutzen und dir eine neue Figur, ein Abenteuer oder eine Botschaft ausdenken.

Eine einfache und schöne Technik, um mit Freude Geschichten zu erfinden, ist die folgende [^2^]:

1. Wähle einen Namen für dein kleines Mädchen aus. Zum Beispiel: Anna, Lena, Mia oder Sophie.
2. Überlege dir, wo deine Geschichte spielen soll. Zum Beispiel: im Wald, im Schloss, im Weltraum oder in der Schule.
3. Überlege dir, was dein kleines Mädchen erleben oder erreichen will. Zum Beispiel: einen Freund finden, einen Schatz entdecken, ein Rätsel lösen oder einen Wunsch erfüllen.
4. Überlege dir, welche Hindernisse oder Gefahren dein kleines Mädchen überwinden muss. Zum Beispiel: einen bösen Wolf, eine Hexe, einen Drachen oder eine Prüfung.
5. Überlege dir, wie deine Geschichte enden soll. Zum Beispiel: mit einem Happy End, einer Überraschung, einer Lehre oder einem offenen Ende.

Wenn du diese Schritte befolgst, hast du schon eine grobe Struktur für deine Geschichte. Dann kannst du sie mit Details, Dialogen und Beschreibungen ausschmücken.

Möchtest du es versuchen? Wie heißt dein kleines Mädchen?
"""))