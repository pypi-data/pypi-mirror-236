import requests
import os
from dotenv import load_dotenv
from typing import Optional
from skymap_stac.item_search import (
    ItemSearch, 
    CollectionsLike, 
    IntersectsLike, 
    DatetimeLike,
    FilterLike,
    SortbyLike,
    Dict,
    Any
)

load_dotenv()

ROLODEX_API_URL='http://192.168.4.204:8080'

class Client:
    def __init__(
        self, 
        url: str, 
        header: Optional[Dict[str, str]] = {'Authorization': f'Bearer {os.getenv("EOF_TOKEN")}'},
        parameters: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        self.url = url
        self.header = header
        self.parameters = parameters
        self.kwargs = kwargs

    @classmethod
    def open(
        cls,
        url: str = f'{ROLODEX_API_URL}/api/cube/datasets',
        headers: Optional[Dict[str, str]] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> "Client":
        """Opens a STAC Catalog or API

        Args:
            url : The URL of a STAC Catalog.
            headers : A dictionary of additional headers to use in all requests
                made to any part of this Catalog/API.
            parameters: Optional dictionary of query string parameters to
                include in all requests.
            
        Return:
            catalog : A :class:`Client` instance for this Catalog/API
        """

        client: Client = cls(
            url=url, 
            headers=headers, 
            parameters=parameters
        )

        return client
        # s = requests.Session()
        # s.headers.update({
        #     'Authorization': f'Bearer {os.getenv("EOF_TOKEN")}',
        # })

        # data = {
        #     "product_name": "sen2",
        #     "aoi": {
        #         "type": "Polygon",
        #         "coordinates": [[
        #             [104.14858238680847, 1.189077295023921],
        #             [103.52866124251142, 1.189077295023921],
        #             [103.52866124251142, 1.5405272307583147],
        #             [104.14858238680847, 1.5405272307583147],
        #             [104.14858238680847, 1.189077295023921]
        #         ]]
        #     },
        #     "time_range": "2023-09-13,2023-09-15"
        # }
        # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ', os.getenv('EOF_TOKEN'))
        # response = s.post(url=url, json=data)
        # return response.json()

    def search(self,
               method: Optional[str] = 'POST',
               max_items: Optional[int] = None, 
               collections: Optional[CollectionsLike] = None, 
               intersects: Optional[IntersectsLike] = None, 
               time_range: Optional[DatetimeLike] = None, 
               filter: Optional[FilterLike] = None, 
               sortby: Optional[SortbyLike] = None
    ) -> "ItemSearch":
        """
        This method returns an :class:`~skymap_stac.ItemSearch` instance. See that
        class's documentation for details on how to get the number of matches and
        iterate over results.

        Args:
            method : The HTTP method to use when making a request to the service.
                This must be either ``"GET"``, ``"POST"``, or
                ``None``. If ``None``, this will default to ``"POST"``.
                If a ``"POST"`` request receives a ``405`` status for
                the response, it will automatically retry with
                ``"GET"`` for all subsequent requests.
            max_items : The maximum number of items to return from the search, even
                if there are more matching results. This client to limit the
                total number of Items returned from the :meth:`items`,
                :meth:`item_collections`, and :meth:`items_as_dicts methods`. The client
                will continue to request pages of items until the number of max items is
                reached. This parameter defaults to 100. Setting this to ``None`` will
                allow iteration over a possibly very large number of results.
            limit: A recommendation to the service as to the number of items to return
                *per page* of results. Defaults to 100.
            ids: List of one or more Item ids to filter on.
            collections: List of one or more Collection IDs or
                :class:`pystac.Collection` instances. Only Items in one
                of the provided Collections will be searched
            bbox: A list, tuple, or iterator representing a bounding box of 2D
                or 3D coordinates. Results will be filtered
                to only those intersecting the bounding box.
            intersects: A string or dictionary representing a GeoJSON geometry, or
                an object that implements a
                ``__geo_interface__`` property, as supported by several libraries
                including Shapely, ArcPy, PySAL, and
                geojson. Results filtered to only those intersecting the geometry.
            datetime: Either a single datetime or datetime range used to filter results.
                You may express a single datetime using a :class:`datetime.datetime`
                instance

                If using a simple date string, the datetime can be specified in
                ``YYYY-mm-dd`` format, optionally truncating
                to ``YYYY-mm`` or just ``YYYY``. Simple date strings will be expanded to
                include the entire time period, for example:

                - ``2017`` expands to ``2017-01-01T00:00:00Z/2017-12-31T23:59:59Z``
                - ``2017-06`` expands to ``2017-06-01T00:00:00Z/2017-06-30T23:59:59Z``
                - ``2017-06-10`` expands to
                  ``2017-06-10T00:00:00Z/2017-06-10T23:59:59Z``

                If used in a range, the format of datetime is year/month/day, 
                for example:
                
                - ``2023-09-13,2023-09-15``

                
            filter: JSON of query parameters as per the STAC API `filter` extension
            sortby: A single field or list of fields to sort the response by

        Returns:
            search : An ItemSearch instance that can be used to iterate through Items.
        """
        return ItemSearch(
            url=self.url,
            method=method,
            header=self.header,
            max_items=max_items,
            collections=collections,
            intersects=intersects,
            time_range=time_range,
            filter=filter,
            sortby=sortby
        )