import re


def levenshtein_distance(a: str, b: str) -> int:
    print(a, b, "BBOOOOBIIIK")
    n = len(a)
    m = len(b)
    if n == 0 or m == 0:
        return n + m
    distance = [[0] * m for i in range(n)]
    for i in range(n):
        distance[i][0] = i
    for i in range(m):
        distance[0][i] = i
    for i in range(1, n):
        for j in range(1, m):
            is_different = 1
            if a[i] == b[j]:
                is_different = 0
            distance[i][j] = min(distance[i][j - 1] + 1, distance[i - 1][j] + 1, distance[i - 1][j - 1] + is_different)
    return distance[n - 1][m - 1]


def search_platforms(search_request: str, platforms_names: list[str]) -> list[str]:
    words_in_request = re.split(r'[ ,.;:_!+@#$|()\"\'\-\\\[\]]+', search_request)
    levenshtein_list = []

    for platform in platforms_names:
        words_in_platform = re.split(r'[ ,.;:_!+@#$|()\"\'\-\\\[\]]+', platform)
        levenshtein_sum = 0
        for request_word in words_in_request:
            best = 1000000
            for platform_word in words_in_platform:
                best = min(best, levenshtein_distance(platform_word, request_word))
            levenshtein_sum += best
        levenshtein_list.append((levenshtein_sum, platform))

    levenshtein_list.sort(key=lambda x: x[0])
    answer = []
    for i in levenshtein_list:
        answer.append(i[1])
    return answer
