from codelimit.common.LanguageTotals import LanguageTotals
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.SourceFileEntry import SourceFileEntry


def test_add():
    lt = LanguageTotals("Python")

    assert lt.language == "Python"
    assert lt.files == 0
    assert lt.loc == 0

    lt.add(SourceFileEntry("foo.py", "abcd1234", "Python", 20,
                           [Measurement("bar()", Location(10, 1), Location(30, 1), 20)]))

    assert lt.files == 1
    assert lt.loc == 20

    lt.add(SourceFileEntry("bar.py", "abcd1234", "Python", 10,
                           [Measurement("spam()", Location(10, 1), Location(20, 1), 10)]))

    assert lt.files == 2
    assert lt.loc == 30


def test_is_equal():
    lt1 = LanguageTotals("Python")
    lt2 = LanguageTotals("Python")

    assert lt1.is_equal(lt2)
    assert lt2.is_equal(lt1)

    lt1.add(SourceFileEntry("foo.py", "abcd1234", "Python", 20,
                            [Measurement("bar()", Location(10, 1), Location(30, 1), 20)]))

    assert not lt1.is_equal(lt2)
    assert not lt2.is_equal(lt1)

    lt2.add(SourceFileEntry("foo.py", "abcd1234", "Python", 20,
                            [Measurement("bar()", Location(10, 1), Location(30, 1), 20)]))

    assert lt1.is_equal(lt2)
    assert lt2.is_equal(lt1)

    lt1.add(SourceFileEntry("bar.py", "abcd1234", "Python", 10,
                            [Measurement("spam()", Location(10, 1), Location(20, 1), 10)]))
    lt2.add(SourceFileEntry("bar.py", "abcd1234", "Python", 11,
                            [Measurement("spam()", Location(10, 1), Location(21, 1), 11)]))

    assert not lt1.is_equal(lt2)

    lt1.add(SourceFileEntry("bar.py", "abcd1234", "Python", 1,
                            [Measurement("eggs()", Location(10, 1), Location(11, 1), 1)]))

    assert not lt1.is_equal(lt2)