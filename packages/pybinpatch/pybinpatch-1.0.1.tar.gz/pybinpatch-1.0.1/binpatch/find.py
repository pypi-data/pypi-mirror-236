
def find(pattern, data):
    pattern_len = len(pattern)
    data_len = len(data)

    # KPM Algorithm
    # Code is based ("copied") off of this video
    # https://www.youtube.com/watch?v=JoF0Z7nVSrA

    lps = [0] * pattern_len

    prevLPS, i = 0, 1

    # Setup LPS to determine prefix/suffix matches

    while i < pattern_len:
        # Values match

        if pattern[i] == pattern[prevLPS]:
            lps[i] = prevLPS + 1
            prevLPS += 1
            i += 1

        # Values differ

        elif prevLPS == 0:
            lps[i] = 0
            i += 1

        else:
            # print(lps)
            prevLPS = lps[prevLPS - 1]

    # Search through the data

    i, j = 0, 0

    while i < data_len:
        if data[i] == pattern[j]:
            # Values matched

            i, j = i + 1, j + 1

        else:
            if j == 0:
                # Values differ

                i += 1
            else:
                j = lps[j - 1]

        if j == pattern_len:
            offset = hex(i - pattern_len)
            print(f'Found pattern at offset: {offset}')
            return offset

    print('Did not find pattern!')
    return None
