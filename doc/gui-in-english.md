# Desktop interface — Literal English Pseudocode (LEP)

[LEP standard](LEP-Standard.md). Sources: gui.py (087811ed1b7f7f6483ee4f235f66917b1ffd4b92) and test_gui.py (eaff3220c072a5a98a9c19fdad2f9a3898003b30). Names, widget options and literal expressions remain identifiable.

~~~text
Import filesystem Path.
Import Empty and Queue from queue.
Import subprocess, system interface, threading and Tk graphical toolkit.

Set ROOT to parent directory of resolved absolute path of this file.
Set background, panel and field colors to #080b13, #101827, #0b1220.
Set cyan, blue and pink to #20f5ff, #387bff, #ff368f.
Set ink, muted and error colors to #e7f5ff, #92a8c5, #ff719a.
Set FONT to DejaVu Sans Mono, eleven points.
Set EXAMPLES to pairs of labels and expressions:
    ARITHMETIC: 2+3*4
    ALGEBRA: 2x+7=19
    QUADRATIC: x^2-5x+6=0
    SYSTEM: x+y=10;x-y=2
    INEQUALITY: 2x+1>5
    DERIVATIVE: diff(x^3+2x,x)
    INTEGRAL: integrate(x^2,x,0,3)
    LIMIT: limit(sin(x)/x,x,0)
    MATRIX: det([[1,2],[3,4]])
    STATISTICS: mean([2,4,6])
    PROBABILITY: binomial_pmf(5,2,1/2)
    PRECISION: approx(pi,50)
Set KEYS to rows of six strings:
    7, 8, 9, /, (, )
    4, 5, 6, *, x, y
    1, 2, 3, -, ^, =
    0, ., pi, +, comma, semicolon
    sqrt(, sin(, cos(, log(, [, ]

Function compute with expression:
    If stripped expression is empty:
        Return false and "Enter a mathematical expression."
    If length of expression exceeds 4096:
        Return false and "Input exceeds 4096 characters."
    Try:
        Set result to run subprocess with argument list containing
            current Python executable, engine.py inside ROOT, expression.
        Set working directory to ROOT.
        Capture output as text, wait at most twenty seconds,
            and do not raise automatically for nonzero exit status.
    If subprocess timeout:
        Return false and timeout message.
    If operating system, Unicode or value error:
        Return false and string of exception.
    Set output to stripped standard output if return code is zero,
        otherwise stripped standard error.
    If output is empty:
        Set output to no-result message if return code is zero,
            otherwise engine-exit message containing return code.
    If length of output exceeds thirty thousand:
        Set output to first thirty thousand characters plus truncation message.
    Return whether return code equals zero, and output.

Class Zer0Calculator:

    Constructor with self and root:
        Store root on self.
        Set title to "ZER0 // UNIVERSAL CALCULATOR".
        Set background to BG.
        Set geometry to 1120 by 760.
        Set minimum size to 760 by 660.
        Create string variable expression.
        Create string variable status initially "READY // LOCAL ENGINE".
        Create results queue.
        Create empty history list.
        Set busy to false.
        Call self.build.
        Bind Enter and Control+Enter to self.solve.
        Bind Control+L to self.clear.
        Schedule self.poll after sixty milliseconds.

    Function label with self, parent, text, color default MUTED, size default ten:
        Return Tk Label with parent and text, foreground color,
            panel background, bold DejaVu Sans Mono at size,
            aligned west.

    Function button with self, parent, text, command, accent default false:
        Return Tk Button with supplied parent, text and command.
        Set background to cyan and foreground to BG if accent,
            otherwise field background and ink foreground.
        Set active background pink and active foreground BG.
        Set disabled foreground muted.
        Set flat relief, zero border, one-pixel highlight,
            blue highlight background and cyan focused highlight.
        Set FONT, horizontal padding eight, vertical padding five,
            hand cursor and keyboard focus enabled.

    Function draw_banner with self and event:
        Set canvas to self.banner.
        Delete all canvas objects.
        Set w and h to event width and height.
        For x from zero to w excluding w, stepping by twenty-six:
            Draw vertical grid line at x with color #14223b.
        For y from zero to h excluding h, stepping by twenty-six:
            Draw horizontal grid line at y with color #14223b.
        For i from zero through eight:
            Set x to w minus one hundred thirty plus thirteen times i.
            Draw blue diagonal from (x, zero) to (x minus thirty-five, h),
                width three.
        Draw blue polygon through (12,14), (34,7), (375,7), (355,18).
        Draw pink bold italic ZER0 // MATH text at (27,48), west anchored.
        Draw cyan bold italic ZER0 // MATH text at (24,45), west anchored.
        Use thirty-point DejaVu Sans for both title layers.
        Draw pink underline through (24,71), (289,68), (318,75), width four.
        Draw ink motto TRUTH GUIDES / INQUIRE EVOLVES at (26,92), west anchored, FONT.
        Draw cyan LOCAL CAS // 0x01 at (w minus twenty,111), east anchored, FONT.

    Function build with self:
        Create banner Canvas in root, height 125, BG, no highlight.
        Pack banner to fill horizontally.
        Bind configure event to self.draw_banner.
        Create body Frame with BG, padding twelve horizontally and eight vertically.
        Pack body to fill both axes and expand.
        Configure body column zero weight three, column one weight one
            and minimum size 218; row zero weight one.
        Create main Frame with PANEL and padding twelve by ten.
        Grid main at row zero, column zero, stretch all directions, right margin eight.
        Create side Frame with PANEL and padding ten by ten.
        Grid side at row zero, column one, stretch all directions.
        Create cyan expression-input label and pack horizontally.
        Create entry in main bound to expression, field background,
            ink foreground, cyan insertion cursor, flat relief,
            sixteen-point mono font, one-pixel blue/cyan focus highlight.
        Pack entry horizontally, internal vertical padding nine, margins five and eight.
        Create controls Frame and pack horizontally.
        Create accent execute button bound to solve; pack left, expand horizontally.
        Create clear and copy buttons bound to their functions; pack left with margins.
        Create pink result-output label and pack with margins.
        Create output frame in main and pack expanding both axes.
        Create disabled Text widget with height five, word wrap, field background,
            cyan foreground, fourteen-point mono font, flat relief, padding eight.
        Create scrollbar linked to output vertical view.
        Link output scroll command to scrollbar set.
        Pack scrollbar on right filling vertically.
        Pack output on left expanding both axes.
        Call show_output with awaiting-input message.
        Create cyan symbol-deck label and pack.
        Create deck Frame and pack horizontally.
        For each of six columns:
            Set equal weight and common uniform group.
        For each indexed row of KEYS:
            For each indexed key of that row:
                Create button labeled key with callback capturing that key
                    and calling insert with it.
                Grid button at its row and column, stretch, two-pixel margins.
        Create cyan math-modules label in side and pack.
        Create examples Frame and pack with margins.
        For each name and sample in EXAMPLES:
            Create button named name with callback capturing sample
                and calling load with it; pack horizontally with one-pixel margin.
        Create pink session-history label and pack.
        Create history Listbox with field background, ink foreground,
            FONT, height five, flat relief, independent selection,
            blue selection background and ink selection foreground.
        Pack history box expanding both axes.
        Bind double-click and Enter on history box to recall.
        Create clear-history button and pack horizontally.
        Create footer Label bound to status, field background,
            cyan foreground, west aligned, FONT, padding twelve by six.
        Pack footer horizontally.
        Focus entry.

    Function insert with self and value:
        If entry selection exists:
            Delete from first selected character to last selected character.
        Insert value at insertion cursor.
        Focus entry.

    Function load with self and value:
        Set expression to value.
        Move entry insertion cursor to end.
        Focus entry.

    Function show_output with self, text and ok default true:
        Enable editing of output and set foreground cyan if ok, otherwise error.
        Delete output from first character to end.
        Insert text at first character.
        Disable editing of output.

    Function solve with self and event default nothing:
        If busy: return "break".
        Set expression to value of self.expression.
        If stripped expression is empty:
            Set status to INPUT REQUIRED.
            Return "break".
        Set busy true.
        Disable solve button.
        Set status to COMPUTING // SYMBOLIC ENGINE.
        Call show_output with Processing...
        Create daemon thread targeting worker with expression as sole argument.
        Start thread.
        Return "break".

    Function worker with self and expression:
        Try: unpack compute of expression into ok and output.
        If exception: set ok false and output to string of exception.
        Put tuple of expression, ok and output into results queue.

    Function poll with self:
        Try:
            Retrieve result from queue without waiting,
                unpack into expression, ok and output.
        If queue empty: do nothing.
        Otherwise:
            Call show_output with output and ok.
            Insert tuple of expression, output and ok at front of history.
            Insert expression at front of history box.
            If history length greater than one hundred:
                Remove last history entry.
                Delete history box item at index one hundred.
            Set busy false.
            Enable solve button.
            Set status to completion and domain warning if ok,
                otherwise error and input warning.
        Schedule poll after sixty milliseconds.

    Function recall with self and event default nothing:
        Set selection to current history box selection.
        If selection exists and not busy:
            Unpack history at first selected index into expression, output, ok.
            Call load with expression.
            Call show_output with output and ok.
            Set status to HISTORY // RECALLED.
        Return "break".

    Function clear_history with self:
        Clear history list.
        Delete history box from index zero to end.

    Function clear with self and event default nothing:
        Call load with empty string.
        If not busy:
            Call show_output with awaiting-input message.
            Set status to READY // LOCAL ENGINE.
        Return "break".

    Function copy with self:
        Set text to output contents from first character to end minus one character.
        Clear root clipboard.
        Append text to root clipboard.
        Set status to OUTPUT COPIED.

Function main:
    Set root to new Tk application.
    Construct Zer0Calculator with root.
    Run root graphical event loop.

If this file is main script: call main.
~~~

## GUI tests

~~~text
Import subprocess and unit testing.
Import patch from unit testing mock.
Import ROOT and compute from gui.

Class ComputeTests inherits unit testing TestCase:
    Function test_arithmetic:
        Assert compute of "2+3*4" equals tuple true, "14".

    Function test_equation:
        Assert compute of "2x+7=19" equals tuple true, "{6}".

    Function test_bad_input:
        Unpack compute of "2+" into ok and message.
        Assert ok false.
        Assert message truthy.

    Replace gui subprocess run with mock for test_validation:
        Assert first element of compute of three spaces false.
        Assert first element of compute of 4097 repetitions of "1" false.
        Assert mock never called.

    Replace gui subprocess run with mock raising timeout for test_timeout:
        Assert first element of compute of "2+2" false.
        Assert mock call working directory equals ROOT.
        Assert mock call timeout equals twenty.

    Replace gui subprocess run with mock for test_argument_vector:
        Set mock return to completed process with return code zero,
            standard output "4" and newline, empty standard error.
        Assert compute of "2+2" equals tuple true, "4".
        Unpack mock call into positional arguments and keyword arguments.
        Assert first positional argument is a list.
        Assert third item of that list equals "2+2".
        Assert shell option false, defaulting to false if absent.

    Replace gui subprocess run with mock for test_output_limit:
        Set mock return to successful completed process with standard output
            containing thirty thousand and one copies of "a", empty standard error.
        Unpack compute of "1" into ok and output.
        Assert ok true.
        Assert output ends with "[Display truncated]".

If this file is main script: call unit testing main.
~~~

LEP describes the source's behavior; it does not establish that the GUI has been rendered or that tests have passed.
