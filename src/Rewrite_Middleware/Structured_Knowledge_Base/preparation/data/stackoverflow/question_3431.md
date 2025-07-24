# Cast option values directly?
[Link to question](https://stackoverflow.com/questions/79354594/cast-option-values-directly)
**Creation Date:** 1736848657
**Score:** 2
**Tags:** postgresql, rust, casting, null
## Question Body
<p>I'm using the <a href="https://crates.io/crates/postgres" rel="nofollow noreferrer">postgres-rs</a> crate to retrieve info from a database. The query result gets stored in a <code>postgres::Row</code> where I can read a value at a time with <a href="https://docs.rs/postgres/latest/postgres/row/struct.Row.html#method.get" rel="nofollow noreferrer"><code>Row::get()</code></a>.</p>
<p>So far so good, but now I want to read a PostgreSQL <code>smallint</code> or <code>i16</code>, and use this value as an <code>i64</code> in Rust. I got it to work with:</p>
<pre class="lang-rust prettyprint-override"><code>let temp: Option&lt;i16&gt; = row.get(index);
let value = if let Some(v) = temp { Some(i64::from(v)) } else { None };
</code></pre>
<p>But it must be because my lack of experience with Rust that I can't write a one liner. I've tried:</p>
<pre class="lang-rust prettyprint-override"><code>let value: Option&lt;i64&gt; = row.get::&lt;Option&lt;i16&gt;&gt;::get(index);
</code></pre>
<p>But that leaves me with an error:</p>
<pre><code>the trait `postgres::row::RowIndex` is not implemented for `std::option::Option&lt;i64&gt;`
</code></pre>
<p>Also I can't seem to cast option values directly:</p>
<pre class="lang-rust prettyprint-override"><code>let value: Option&lt;usize&gt; = Some(1 as i16).into();
</code></pre>
<p>This also gives me a similar error:</p>
<pre><code>the trait `From&lt;Option&lt;i16&gt;&gt;` is not implemented for `Option&lt;usize&gt;`
</code></pre>
<p>I assume these errors are by design, but I'm still wondering if there isn't a shorter or better way to rewrite my first working example.</p>

## Answers
### Answer ID: 79357618
<p><code>Row::get()</code> takes two generic type arguments: <code>I</code>, type of the index, and <code>T</code>, type of the return vaue. Your attempt to specify the type argument sets the first one, which is <code>I</code>, whereas you meant to set <code>T</code>. This is why you get the error that &quot;trait <code>RowIndex</code> is not implemented for <code>Option&lt;i64&gt;</code>&quot;. You need to use <code>_</code> to leave it to the compiler to infer <code>I</code>:</p>
<pre><code>let value: Option&lt;i64&gt; = row.get::&lt;_, Option&lt;i16&gt;&gt;(index).map(Into::into);
</code></pre>
<p>Your other issue that you try to convert to <code>usize</code> using the <code>From</code> (or <code>Into</code>) trait, which doesn't work because <code>From</code> is for conversions that can't fail. Since there are <code>i16</code> values that can't be represented as <code>usize</code> (all the negative ones), <code>From&lt;i16&gt;</code> is not implemented for <code>usize</code>. Instead, you need to use <a href="https://doc.rust-lang.org/std/convert/trait.TryFrom.html" rel="nofollow noreferrer"><code>TryFrom</code></a>, which is, and handle errors accordingly.</p>

