import tools_karkkainen_sanders as tks
import unittest


def longest(s):
    '''
    longest repeating substring
    '''
    sa = tks.simple_kark_sort(s)
    lcp = tks.LCP(s, sa)
    maxI, maxV = -1, -1
    for i, v in enumerate(lcp):
        if v > maxV:
            maxI, maxV = i, v
    return s[sa[maxI]:sa[maxI] + maxV]


def search(P, sStr):
    '''
    find first substring P
    '''
    sa = tks.simple_kark_sort(sStr)
    m = len(P)
    n = len(sStr)
    left,  right = 0, n  # length of sa is n+1
    while left < right:
        mid = (left + right) >> 1
        comp = cmp(sStr[sa[mid]:sa[mid] + m], P)
        if comp >= 0:
            right = mid
        else:
            left = mid + 1
    if sStr[sa[left]: sa[left] + m] == P:
        return sa[left]
    else:
        return -1


def search2(P, sStr):
    '''
    find the substring P, all occurances
    '''
    sa = tks.simple_kark_sort(sStr)
    m = len(P)
    n = len(sStr)
    start, end = -1, -1
    # lower bound
    left,  right = 0, n  # length of sa is n+1
    while left < right:
        mid = (left + right) >> 1
        comp = cmp(sStr[sa[mid]:sa[mid] + m], P)
        if comp >= 0:
            right = mid
        else:
            left = mid + 1
    start = left
    if sStr[sa[left]: sa[left] + m] != P:
        return []

    # upper bound
    left,  right = 0, n  # length of sa is n+1
    while left < right:
        mid = (left + right) >> 1
        comp = cmp(sStr[sa[mid]:sa[mid] + m], P)
        if comp > 0:
            right = mid
        else:
            left = mid + 1
    end = left
    result = [sa[i] for i in range(start, end)]
    result.sort()
    return result


class testUtility(unittest.TestCase):

    def test_longest(self):
        s = 'aaaabcaa'
        self.assertEquals(longest(s), 'aaa')

    def test_search(self):
        s = 'a' * 8
        occurance = search('ba', s)
        self.assertEquals(occurance, -1)

        occurance = search('acd', s)
        self.assertEquals(occurance, -1)

        occurance = search('aaaa', s)
        self.assertEquals(occurance, 4)

    def test_search2(self):
        s = 'a' * 8
        occurance = search2('ba', s)
        self.assertEquals(occurance, [])

        occurance = search2('aaa', s)
        self.assertEquals(occurance, range(6))


if __name__ == '__main__':
    unittest.main()
