import sched, time
import urllib
from urllib.request import URLError
s = sched.scheduler(time.time, time.sleep)
def do_something(sc):

    result_url = []
    count = 0
    not_200 = 0
    f = open("urllist.txt", "r")
    img_not_200 = open("img_not_200.txt", "w+")
    for line in f:
        count += 1
        print("on scanning ", count)
        try:
            response = urllib.request.urlopen(line)
        except URLError as e:
            if hasattr(e, 'reason'):  # stands for URLError
                print("can not reach a server,writing...")
                result_url.append(line)
                not_200 += 1
                img_not_200.write(line)
                print("write url success!")
            elif hasattr(e, 'code'):  # stands for HTTPError
                print("find http error, writing...")
                result_url.append(line)
                not_200 += 1
                img_not_200.write(line)
                print("write url success!")
            else:  # stands for unknown error
                print("unknown error, writing...")
                result_url.append(line)
                not_200 += 1
                img_not_200.write(line)
                print("write url success!")
        else:
            # print "url is reachable!"
            # else 中不用再判断 response.code 是否等于200,若没有抛出异常，肯定返回200,直接关闭即可
            response.close()
        finally:
            print(line)
            pass
    print("scanning over,total", count, "; did not response 200:", not_200)
    f.close()
    img_not_200.close()
    s.enter(5, 1, do_something, (sc,))

s.enter(5, 1, do_something, (s,))
s.run()