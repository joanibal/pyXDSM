import unittest
import os

from pyxdsm.XDSM import XDSM


class TestXDSM(unittest.TestCase):

    def setUp(self):
        import os
        import tempfile

        self.startdir = os.getcwd()
        self.tempdir = tempfile.mkdtemp(prefix='testdir-')

        os.chdir(self.tempdir)

    def tearDown(self):
        import os
        import shutil

        os.chdir(self.startdir)

        try:
            shutil.rmtree(self.tempdir)
        except OSError:
            pass

    def test_options(self):

        filename = 'xdsm_test_options'
        spec_dir = filename + '_specs'

        # Change `use_sfmath` to False to use computer modern
        x = XDSM(use_sfmath=False)

        x.add_system('opt', 'Optimization', r'\text{Optimizer}')
        x.add_system('solver', 'MDA', r'\text{Newton}')
        x.add_system('D1', 'Function', 'D_1', text_width=2.0)
        x.add_system('D2', 'Function', 'D_2', stack=False)
        x.add_system('F', 'Function', 'F', faded=True)
        x.add_system('G', 'Function', 'G', spec_name="G_spec")

        x.connect('opt', 'D1', 'x, z')
        x.connect('opt', 'D2', 'z')
        x.connect('opt', 'F', 'x, z')
        x.connect('solver', 'D1', 'y_2')
        x.connect('solver', 'D2', 'y_1')
        x.connect('D1', 'solver', r'\mathcal{R}(y_1)')
        x.connect('solver', 'F', 'y_1, y_2')
        x.connect('D2', 'solver', r'\mathcal{R}(y_2)')
        x.connect('solver', 'G', 'y_1, y_2')

        x.connect('F', 'opt', 'f')
        x.connect('G', 'opt', 'g')

        x.add_output('opt', 'x^*, z^*', side='right')
        x.add_output('D1', 'y_1^*', side='left', stack=True)
        x.add_output('D2', 'y_2^*', side='left')
        x.add_output('F', 'f^*', side='left')
        x.add_output('G', 'g^*')
        x.write(filename)
        x.write_sys_specs(spec_dir)

        # Test if files where created
        self.assertTrue(os.path.isfile(filename + '.tikz'))
        self.assertTrue(os.path.isfile(filename + '.tex'))
        self.assertTrue(os.path.isdir(spec_dir))
        self.assertTrue(os.path.isfile(os.path.join(spec_dir, 'F.json')))
        self.assertTrue(os.path.isfile(os.path.join(spec_dir, 'G_spec.json')))

    def test_tikz_content(self):
        # Check if TiKZ file was created.
        # Compare the content of the sample below and the newly created TiKZ file.

        tikz_txt = r"""
            
            %%% Preamble Requirements %%%
            % \usepackage{geometry}
            % \usepackage{amsfonts}
            % \usepackage{amsmath}
            % \usepackage{amssymb}
            % \usepackage{tikz}
            
            % Optional packages such as sfmath set through python interface
            % \usepackage{sfmath}
            
            % \usetikzlibrary{arrows,chains,positioning,scopes,shapes.geometric,shapes.misc,shadows}
            
            %%% End Preamble Requirements %%%
            
            \input{"D:/Documents/GitHub/mypyXDSM/pyXDSM/pyxdsm/diagram_styles"}
            \begin{tikzpicture}
            
            \matrix[MatrixSetup]{
            %Row 0
            \node [DataIO] (left_output_opt) {$x^*, z^*$};&
            \node [Optimization] (opt) {$\text{Optimizer}$};&
            &
            \node [DataInter] (opt-D1) {$x, z$};&
            \node [DataInter] (opt-D2) {$z$};&
            \node [DataInter] (opt-F) {$x, z$};&
            \\
            %Row 1
            &
            &
            \node [MDA] (solver) {$\text{Newton}$};&
            \node [DataInter] (solver-D1) {$y_2$};&
            \node [DataInter] (solver-D2) {$y_1$};&
            \node [DataInter] (solver-F) {$y_1, y_2$};&
            \node [DataInter] (solver-G) {$y_1, y_2$};\\
            %Row 2
            \node [DataIO] (left_output_D1) {$y_1^*$};&
            &
            \node [DataInter] (D1-solver) {$\mathcal{R}(y_1)$};&
            \node [Function] (D1) {$D_1$};&
            &
            &
            \\
            %Row 3
            \node [DataIO] (left_output_D2) {$y_2^*$};&
            &
            \node [DataInter] (D2-solver) {$\mathcal{R}(y_2)$};&
            &
            \node [Function] (D2) {$D_2$};&
            &
            \\
            %Row 4
            \node [DataIO] (left_output_F) {$f^*$};&
            \node [DataInter] (F-opt) {$f$};&
            &
            &
            &
            \node [Function] (F) {$F$};&
            \\
            %Row 5
            \node [DataIO] (left_output_G) {$g^*$};&
            \node [DataInter] (G-opt) {$g$};&
            &
            &
            &
            &
            \node [Function] (G) {$G$};\\
            %Row 6
            &
            &
            &
            &
            &
            &
            \\
            };
            
            % XDSM process chains
            
            
            \begin{pgfonlayer}{data}
            \path
            % Horizontal edges
            (opt) edge [DataLine] (opt-D1)
            (opt) edge [DataLine] (opt-D2)
            (opt) edge [DataLine] (opt-F)
            (solver) edge [DataLine] (solver-D1)
            (solver) edge [DataLine] (solver-D2)
            (D1) edge [DataLine] (D1-solver)
            (solver) edge [DataLine] (solver-F)
            (D2) edge [DataLine] (D2-solver)
            (solver) edge [DataLine] (solver-G)
            (F) edge [DataLine] (F-opt)
            (G) edge [DataLine] (G-opt)
            (opt) edge [DataLine] (left_output_opt)
            (D1) edge [DataLine] (left_output_D1)
            (D2) edge [DataLine] (left_output_D2)
            (F) edge [DataLine] (left_output_F)
            (G) edge [DataLine] (left_output_G)
            % Vertical edges
            (opt-D1) edge [DataLine] (D1)
            (opt-D2) edge [DataLine] (D2)
            (opt-F) edge [DataLine] (F)
            (solver-D1) edge [DataLine] (D1)
            (solver-D2) edge [DataLine] (D2)
            (D1-solver) edge [DataLine] (solver)
            (solver-F) edge [DataLine] (F)
            (D2-solver) edge [DataLine] (solver)
            (solver-G) edge [DataLine] (G)
            (F-opt) edge [DataLine] (opt)
            (G-opt) edge [DataLine] (opt);
            \end{pgfonlayer}
            
            \end{tikzpicture}"""

        def filter_lines(lns):
            # Empty lines are excluded.
            # Leading and trailing whitespaces are removed
            # Comments are removed.
            return [ln.strip() for ln in lns if ln.strip() and not ln.strip().startswith('%')]

        filename = 'xdsm_test_tikz'

        x = XDSM(use_sfmath=True)

        x.add_system('opt', 'Optimization', r'\text{Optimizer}')
        x.add_system('solver', 'MDA', r'\text{Newton}')
        x.add_system('D1', 'Function', 'D_1')
        x.add_system('D2', 'Function', 'D_2')
        x.add_system('F', 'Function', 'F')
        x.add_system('G', 'Function', 'G')

        x.connect('opt', 'D1', 'x, z')
        x.connect('opt', 'D2', 'z')
        x.connect('opt', 'F', 'x, z')
        x.connect('solver', 'D1', 'y_2')
        x.connect('solver', 'D2', 'y_1')
        x.connect('D1', 'solver', r'\mathcal{R}(y_1)')
        x.connect('solver', 'F', 'y_1, y_2')
        x.connect('D2', 'solver', r'\mathcal{R}(y_2)')
        x.connect('solver', 'G', 'y_1, y_2')

        x.connect('F', 'opt', 'f')
        x.connect('G', 'opt', 'g')

        x.add_output('opt', 'x^*, z^*', side='left')
        x.add_output('D1', 'y_1^*', side='left')
        x.add_output('D2', 'y_2^*', side='left')
        x.add_output('F', 'f^*', side='left')
        x.add_output('G', 'g^*', side='left')
        x.write(filename)

        # Check if file was created
        tikz_file = filename + '.tikz'

        self.assertTrue(os.path.isfile(tikz_file))

        tikz_lines = tikz_txt.split('\n')
        tikz_lines = filter_lines(tikz_lines)

        with open(tikz_file, "r") as f:
            lines = filter_lines(f.readlines())

        sample_no_match = []  # Sample text
        new_no_match = []  # New text

        for line1, line2 in zip(lines, tikz_lines):
            if line1 != line2:  # else everything is okay
                # This can be because of the different ordering of lines or because of an error.
                sample_no_match.append(line1)
                new_no_match.append(line2)

        # Sort both sets of suspicious lines
        sample_no_match.sort()
        new_no_match.sort()

        for line1, line2 in zip(sample_no_match, new_no_match):
            # Now the lines should match, if only the ordering was different
            self.assertEqual(line1, line2)

        # To be sure, check the length, otherwise a missing last line could get unnoticed because of using zip
        self.assertEqual(len(lines), len(tikz_lines))


if __name__ == "__main__":
    unittest.main()
