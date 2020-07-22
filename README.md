# Interpreter From Scratch!
<h4>Interpreter vs Compiler</h4>
<img src='images/interpreter.png' width='800' />
<h3>What language is the interpreter for? </h3>
<h5>A made up language which closely resembles the syntax for the language <code>BASIC</code>.</h5>
<h3> Grammar For the language and the parser </h3>
<img src='images/Screenshot 2020-07-22 at 2.06.41 PM.png' width='800' />
<h3> Type of Parser </h3>
<h5><code>Recursive Descent Parser with Backtracking</code></h5>
<h3> Error Handling </h3>
<h5>Errors are detected and reported with traceback and even the position of the occuerence of the error in a particular line</h5>
<h5>Types of Errors: </h5>
<ol>
  <code><b>
  <li> InvalidSyntaxError </li>
  <li> RunTimeError </li>
  <li> IllegalCharError </li>
  <li> UnexpectedCharError </li>
    </b></code>
</ol>
<img src='images/Screenshot 2020-07-22 at 2.15.54 PM.png' width='800' />
<h3> Features </h3>
<ul>
  <h4>1. Math Operations (Add, subtract, multiply, divide, exponentiation) with both <code>int</code> and <code>float</code> types</h4>
  <img src='images/Screenshot 2020-07-22 at 1.34.19 PM.png' width='600' />
  <h4>2. Support for variable assignments of <code>int</code>, <code>float</code>, <code>string</code>, <code>list</code> and even <code>functions</code></h4>
  <img src='images/Screenshot 2020-07-22 at 1.39.19 PM.png' width='600' />
  <h4> 3. Support for string operations </h4>
  <ol>
    <li>Supports <code>string</code> concatenation</li>
    <li>Supports repeating the <code>string</code></li>
  </ol>
   <img src='images/Screenshot 2020-07-22 at 1.43.05 PM.png' width='600' />
  <h4> 4. Support for <code>List</code> operations and the list is generic and supports nesting! </h4>
  <ol>
    <li>Supports negative <code>indexing</code></li>
    <li>Supports <code>appending</code> the <code>list</code> with an element</li>
    <li>Supports <code>extending</code> the <code>list</code> with another <code>list</code></li>
    <li>Supports <code>popping</code> the <code>list</code> with valid <code>indexes</code></li>
  </ol>
   <img src='images/Screenshot 2020-07-22 at 1.48.17 PM.png' width='600' />
  <h5> 5. Support for Conditional statements </h5>
  <ol>
    <li>Supports <code>IF</code>, <code>ELIF</code> and <code>ELSE</code></li>
    <li>Nesting upto any level</li>
    <li>Can even assign variables the <code>expr</code> of the <code>if-else</code> ladder like a <code>terenary operation</code></li>
  </ol>
   <img src='images/Screenshot 2020-07-22 at 1.57.01 PM.png' width='600' />
  <h5> 5. Support for Loops </h5>
  <ol>
    <li><code>FOR</code> and <code>WHILE</code> loops are supported</li>
    <li>Can set the step of the iterable in the <code>FOR</code> loop</li>
    <li> Can store the result of the loops in a <code>list</code> </li>
  </ol>
   <img src='images/Screenshot 2020-07-22 at 2.06.09 PM.png' width='600' />
</ul> 
