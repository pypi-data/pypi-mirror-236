from typing import (Optional, Union, List, Iterator, Protocol, Dict, Any, Tuple)
from datetime import datetime as datetime_
import requests

class GeoInterface(Protocol):
    @property
    def __geo_interface__(self) -> Dict[str, Any]:
        ...

Collections = Tuple[str, ...]
CollectionsLike = Union[List[str], Iterator[str], str]

Intersects = Dict[str, Any]
IntersectsLike = Union[str, GeoInterface, Intersects]

DatetimeOrTimestamp = Optional[Union[datetime_, str]]
Datetime = str
DatetimeLike = Union[
    DatetimeOrTimestamp,
    Tuple[DatetimeOrTimestamp, DatetimeOrTimestamp],
    List[DatetimeOrTimestamp],
    Iterator[DatetimeOrTimestamp],
    str
]

FilterLike = Union[Dict[str, Any], str]

Sortby = List[Dict[str, str]]
SortbyLike = Union[Sortby, str, List[str]]


class ItemSearch:
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

                If used in a range, the end of the range expands to the end of that
                day/month/year, for example:

                - ``2017/2018`` expands to
                  ``2017-01-01T00:00:00Z/2018-12-31T23:59:59Z``
                - ``2017-06/2017-07`` expands to
                  ``2017-06-01T00:00:00Z/2017-07-31T23:59:59Z``
                - ``2017-06-10/2017-06-11`` expands to
                  ``2017-06-10T00:00:00Z/2017-06-11T23:59:59Z``
            filter: JSON of query parameters as per the STAC API `filter` extension
            sortby: A single field or list of fields to sort the response by
        """
    
    def __init__(
        self,
        url: str,
        method: Optional[str] = 'POST',
        header: Dict = None,
        max_items: Optional[int] = None, 
        collections: Optional[CollectionsLike] = None, 
        intersects: Optional[IntersectsLike] = None, 
        time_range: Optional[DatetimeLike] = None, 
        filter: Optional[FilterLike] = None, 
        sortby: Optional[SortbyLike] = None
    ) -> None:
        self.url = url
        self.method = method

        payload = {
            "product_name": collections,
            "aoi": intersects,
            "time_range": time_range
        }

        self.response = requests.request(
            method=method,
            url=url,
            headers=header,
            json=payload
        )

    def get_all_items(self):
        return self.response.json()