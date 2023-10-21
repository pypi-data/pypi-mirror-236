1 ModisDownload
===============

help ours down load from base url
https://ladsweb.modaps.eosdis.nasa.gov/ when i use this packages , our
bandwidth work in deadline with the first version we can use this
download all modis file with any time in any area use like this

2 Example code
==============

2.1 Query Productions
---------------------
We can query productions which can
be downloaded by our **API** or get from **{your ModisDownload package
install directory}/temp/sensor.csv**

.. code:: python

   # search products which can be downloaded
   from ModisDownload.Visited import search_p

   if __name__ == '__main__':
       search_p()

2.2 Query Area Names
--------------------

We can query productions which can be downloaded by our **API** or get
from **{your ModisDownload package install
directory}/temp/country.json**

.. code:: python

   # search products which can be downloaded
   from ModisDownload.Visited import search_area

   if __name__ == '__main__':
       search_area()

2.3 Download products
---------------------

.. code:: python

   # download data main class
   from ModisDownload.Visited import GetHtml

   if __name__ == '__main__':
       # get your token in https://ladsweb.modaps.eosdis.nasa.gov/#generate-token
       token = "your token can be found in https://ladsweb.modaps.eosdis.nasa.gov/#generate-token"

       # init download main class
       obj = GetHtml()

       # set your product name
       product_name = "Mod04_3k"

       # set your query dates
       # query one day use 2020-01-01
       # query dates use start_time..end_time like 2021-01-01..2022-01-01
       # query multi dates like 2020-01-01,2021-01-01..2022-01-01,... and so on
       query_dates = "2020-01-01,2021-01-01..2021-02-01"

       # query area can use name of country or longitude and latitude
       # county like china or other names,you can see all names by search_area() in ModisDownload.Visited
       # area by longitude and latitude like
       # (longitude,latitude)
       # (a,b) ----------
       #       -        -
       #       -        -
       #       -        -
       #       ---------- (c,d)
       # area like xayb,xcyd
       area = "x120y40,x140y20"

       # download files save directory
       save_dir = "./download"

       # thread number default 5
       thread_num = 5

       # max try number if your net close download will be shutdown, 
       # so we will retry some time to make sure download success,default max try number is 10
       max_try = 10

       # if you use proxy you should set you proxy port if port is None not use proxy default port is None
       port = None

       # chunk size is stream I/O size don't change
       chunk_size = 1 << 20

       # download main function
       obj.download_main(sensor_name=product_name, dates=query_dates, area=area, download_dir=save_dir,
                         thread_num=thread_num,
                         max_try=max_try, port=port, chunk_size=chunk_size)

       # only need download urls
       obj.download_main_url(sensor_name=product_name, dates=query_dates, area=area, download_dir=save_dir,
                             save_dir="your downloads urls save path")

2.4 Update ModisDownload
------------------------

update productions names and area

.. code:: python

   # reinit package
   from ModisDownload.Visited import reload

   if __name__ == '__main__':
       reload()
