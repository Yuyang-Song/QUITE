# How to only edit specific bytes of byte of a file instead of rewriting the whole file
[Link to question](https://stackoverflow.com/questions/76934026/how-to-only-edit-specific-bytes-of-byte-of-a-file-instead-of-rewriting-the-whole)
**Creation Date:** 1692430208
**Score:** 0
**Tags:** file, go, filehandler
## Question Body
<p>I wanted to create a single file database for storing bytes which emulates the way our filesystem works on a hard drive such that I am able to edit specific bytes (changed or saved by the user) while writing to the database instead of reading the whole file into memory changing a few bytes and rewriting the database file back to the disk.</p>
<p>How can I just alter specific bytes in the file using the file handler instead of requiring me loading the whole database into memory, doing the changes (this does not change the size of the overall file) and then storing it back.</p>
<p>I have tried searching my query but I am unable to get the answer I am looking for. I have tried using different modes for opening a file handler and maybe trying that.</p>

## Answers
### Answer ID: 76934210
<p>Try to use <a href="https://pkg.go.dev/os#File.WriteAt" rel="nofollow noreferrer">WriteAt</a>:</p>
<pre><code>package main

import (
    &quot;fmt&quot;
    &quot;log&quot;
    &quot;os&quot;
)

const fileName = &quot;test.txt&quot;

func createFile(filename string) error {
    f, err := os.OpenFile(filename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        return fmt.Errorf(&quot;cannot create file: %v&quot;, err)
    }
    defer f.Close()

    if _, err := f.Write([]byte(&quot;Hello, World!&quot;)); err != nil {
        return fmt.Errorf(&quot;cannot write data to file: %v&quot;, err)
    }

    return nil
}

func changeFileByte(filename string, b []byte, pos int64) error {
    f, err := os.OpenFile(filename, os.O_WRONLY, 0644)
    if err != nil {
        return fmt.Errorf(&quot;cannot open file: %v&quot;, err)
    }
    defer f.Close()

    if _, err := f.WriteAt(b, pos); err != nil {
        return fmt.Errorf(&quot;cannot write to file: %v&quot;, err)
    }

    return nil
}

func printFile(filename string) error {
    content, err := os.ReadFile(filename)
    if err != nil {
        return fmt.Errorf(&quot;cannot read file: %v&quot;, err)
    }
    fmt.Printf(&quot;%s\n&quot;, content)

    return nil
}

func main() {
    if err := createFile(fileName); err != nil {
        log.Fatal(err)
    }

    if err := printFile(fileName); err != nil {
        log.Fatal(err)
    }

    if err := changeFileByte(fileName, []byte{'.'}, 12); err != nil {
        log.Fatal(err)
    }

    if err := printFile(fileName); err != nil {
        log.Fatal(err)
    }
}
</code></pre>

