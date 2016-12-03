from __future__ import print_function
import os
import glob

from . import sourmash_tst_utils as utils
try:
    import matplotlib
    matplotlib.use('Agg')
except ImportError:
    pass

from sourmash_lib import signature

def test_run_sourmash():
    status, out, err = utils.runscript('sourmash', [], fail_ok=True)
    assert status != 0                    # no args provided, ok ;)


def test_do_sourmash_compute():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', testdata1],
                                           in_directory=location)
        assert os.path.exists(os.path.join(location, 'short.fa.sig'))


def test_do_sourmash_compute_multik():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', '-k', '21,31',
                                            testdata1],
                                           in_directory=location)
        outfile = os.path.join(location, 'short.fa.sig')
        assert os.path.exists(outfile)

        with open(outfile, 'rt') as fp:
            sigdata = fp.read()
            siglist = signature.load_signatures(sigdata)
            assert len(siglist) == 2
            ksizes = set([ x.estimator.ksize for x in siglist ])
            assert 21 in ksizes
            assert 31 in ksizes


def test_do_sourmash_compute_multik_with_protein():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', '-k', '21,31',
                                            '--protein',
                                            testdata1],
                                           in_directory=location)
        outfile = os.path.join(location, 'short.fa.sig')
        assert os.path.exists(outfile)

        with open(outfile, 'rt') as fp:
            sigdata = fp.read()
            siglist = signature.load_signatures(sigdata)
            assert len(siglist) == 4
            ksizes = set([ x.estimator.ksize for x in siglist ])
            assert 21 in ksizes
            assert 31 in ksizes


def test_do_sourmash_compute_multik_with_nothing():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', '-k', '21,31',
                                            '--no-protein', '--no-dna',
                                            testdata1],
                                           in_directory=location,
                                           fail_ok=True)
        outfile = os.path.join(location, 'short.fa.sig')
        assert not os.path.exists(outfile)


def test_do_sourmash_compute_multik_only_protein():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', '-k', '21,31',
                                            '--protein', '--no-dna',
                                            testdata1],
                                           in_directory=location)
        outfile = os.path.join(location, 'short.fa.sig')
        assert os.path.exists(outfile)

        with open(outfile, 'rt') as fp:
            sigdata = fp.read()
            siglist = signature.load_signatures(sigdata)
            assert len(siglist) == 2
            ksizes = set([ x.estimator.ksize for x in siglist ])
            assert 21 in ksizes
            assert 31 in ksizes


def test_do_sourmash_compute_multik_input_is_protein():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('ecoli.faa.gz')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', '-k', '21,31',
                                            '--input-is-protein',
                                            testdata1],
                                           in_directory=location)
        outfile = os.path.join(location, 'ecoli.faa.gz.sig')
        assert os.path.exists(outfile)

        with open(outfile, 'rt') as fp:
            sigdata = fp.read()
            siglist = signature.load_signatures(sigdata)
            assert len(siglist) == 2
            ksizes = set([ x.estimator.ksize for x in siglist ])
            assert 21 in ksizes
            assert 31 in ksizes

            moltype = set([ x.estimator.is_molecule_type('protein')
                            for x in siglist ])
            assert len(moltype) == 1
            assert True in moltype


def test_do_sourmash_compute_multik_outfile():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa')
        outfile = os.path.join(location, 'FOO.xxx')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', '-k', '21,31',
                                            testdata1, '-o', outfile],
                                           in_directory=location)
        assert os.path.exists(outfile)

        with open(outfile, 'rt') as fp:
            sigdata = fp.read()
            siglist = signature.load_signatures(sigdata)
            assert len(siglist) == 2
            ksizes = set([ x.estimator.ksize for x in siglist ])
            assert 21 in ksizes
            assert 31 in ksizes


def test_do_plot_comparison():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa')
        testdata2 = utils.get_test_data('short2.fa')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', testdata1, testdata2],
                                           in_directory=location)

    
        status, out, err = utils.runscript('sourmash',
                                           ['compare', 'short.fa.sig',
                                            'short2.fa.sig', '-o', 'cmp'],
                                           in_directory=location)

        status, out, err = utils.runscript('sourmash', ['plot', 'cmp'],
                                           in_directory=location)

        assert os.path.exists(os.path.join(location, "cmp.dendro.png"))
        assert os.path.exists(os.path.join(location, "cmp.matrix.png"))


def test_do_plot_comparison_2():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa')
        testdata2 = utils.get_test_data('short2.fa')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', testdata1, testdata2],
                                           in_directory=location)

    
        status, out, err = utils.runscript('sourmash',
                                           ['compare', 'short.fa.sig',
                                            'short2.fa.sig', '-o', 'cmp'],
                                           in_directory=location)

        status, out, err = utils.runscript('sourmash',
                                           ['plot', 'cmp', '--pdf'],
                                           in_directory=location)
        assert os.path.exists(os.path.join(location, "cmp.dendro.pdf"))
        assert os.path.exists(os.path.join(location, "cmp.matrix.pdf"))


def test_do_plot_comparison_3():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa')
        testdata2 = utils.get_test_data('short2.fa')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', testdata1, testdata2],
                                           in_directory=location)

    
        status, out, err = utils.runscript('sourmash',
                                           ['compare', 'short.fa.sig',
                                            'short2.fa.sig', '-o', 'cmp'],
                                           in_directory=location)

        status, out, err = utils.runscript('sourmash',
                                           ['plot', 'cmp', '--labels'],
                                           in_directory=location)

        assert os.path.exists(os.path.join(location, "cmp.dendro.png"))
        assert os.path.exists(os.path.join(location, "cmp.matrix.png"))


def test_sourmash_search():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa')
        testdata2 = utils.get_test_data('short2.fa')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', testdata1, testdata2],
                                           in_directory=location)



        status, out, err = utils.runscript('sourmash',
                                           ['search', 'short.fa.sig',
                                            'short2.fa.sig'],
                                           in_directory=location)
        print(status, out, err)
        assert '1 matches' in out
        assert '0.958' in out


def test_sourmash_search_2():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa')
        testdata2 = utils.get_test_data('short2.fa')
        testdata3 = utils.get_test_data('short3.fa')
        status, out, err = utils.runscript('sourmash',
                                           ['compute', testdata1, testdata2,
                                            testdata3],
                                           in_directory=location)



        status, out, err = utils.runscript('sourmash',
                                           ['search', 'short.fa.sig',
                                            'short2.fa.sig', 'short3.fa.sig'],
                                           in_directory=location)
        print(status, out, err)
        assert '2 matches' in out
        assert '0.958' in out


def test_mash_csv_to_sig():
    with utils.TempDirectory() as location:
        testdata1 = utils.get_test_data('short.fa.msh.dump')
        testdata2 = utils.get_test_data('short.fa')

        status, out, err = utils.runscript('sourmash', ['import_csv',
                                                        testdata1,
                                                        '-o', 'xxx.sig'],
                                           in_directory=location)
        
        status, out, err = utils.runscript('sourmash',
                                           ['compute', '-k', '31', testdata2],
                                           in_directory=location)

        status, out, err = utils.runscript('sourmash',
                                           ['search', '-k', '31',
                                            'short.fa.sig', 'xxx.sig'],
                                           in_directory=location)
        print(status, out, err)
        assert '1 matches:' in out
