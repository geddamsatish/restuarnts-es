#!/usr/bin/env python3
"""
Sample Elasticsearch queries for restaurants data.

Demonstrates various query types: text search, filters, geo queries, aggregations.
"""

import json
import requests
from typing import Dict, List, Any


class RestaurantQueries:
    """Sample queries for restaurant data."""

    def __init__(self, es_url: str = 'http://localhost:9200', index: str = 'restaurants'):
        """
        Initialize query helper.

        Args:
            es_url: Elasticsearch server URL
            index: Index name
        """
        self.es_url = es_url.rstrip('/')
        self.index = index
        self.session = requests.Session()

    def _execute_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Execute query and return results."""
        url = f'{self.es_url}/{self.index}/_search'
        response = self.session.post(
            url,
            json=query,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()

    def search_by_name(self, name: str, size: int = 10) -> Dict[str, Any]:
        """
        Search restaurants by name.

        Args:
            name: Restaurant name or partial name
            size: Number of results to return

        Returns:
            Search results
        """
        query = {
            'size': size,
            'query': {
                'match': {
                    'name': {
                        'query': name,
                        'fuzziness': 'AUTO'
                    }
                }
            }
        }
        return self._execute_query(query)

    def filter_by_cuisine(self, cuisine: str, min_rating: float = 0, size: int = 10) -> Dict[str, Any]:
        """
        Filter restaurants by cuisine and optional minimum rating.

        Args:
            cuisine: Cuisine type (e.g., 'Italian', 'Chinese')
            min_rating: Minimum rating filter
            size: Number of results to return

        Returns:
            Filtered results
        """
        query = {
            'size': size,
            'query': {
                'bool': {
                    'must': [
                        {'term': {'cuisine': cuisine}}
                    ],
                    'filter': [
                        {'range': {'rating': {'gte': min_rating}}}
                    ]
                }
            }
        }
        return self._execute_query(query)

    def search_text(self, text: str, fields: List[str] = None, size: int = 10) -> Dict[str, Any]:
        """
        Full-text search across multiple fields.

        Args:
            text: Search text
            fields: Fields to search (default: name, description, address)
            size: Number of results to return

        Returns:
            Search results
        """
        if fields is None:
            fields = ['name^2', 'description', 'address']

        query = {
            'size': size,
            'query': {
                'multi_match': {
                    'query': text,
                    'fields': fields,
                    'type': 'best_fields',
                    'operator': 'or'
                }
            }
        }
        return self._execute_query(query)

    def geo_search(self, latitude: float, longitude: float, distance: str = '5km', size: int = 20) -> Dict[str, Any]:
        """
        Find restaurants within a distance from a location.

        Args:
            latitude: Center latitude
            longitude: Center longitude
            distance: Search radius (e.g., '5km', '10km', '1mi')
            size: Number of results to return

        Returns:
            Nearby restaurants
        """
        query = {
            'size': size,
            'query': {
                'bool': {
                    'must': [
                        {
                            'geo_distance': {
                                'distance': distance,
                                'location': {
                                    'lat': latitude,
                                    'lon': longitude
                                }
                            }
                        }
                    ]
                }
            },
            'sort': [
                {
                    '_geo_distance': {
                        'location': {
                            'lat': latitude,
                            'lon': longitude
                        },
                        'order': 'asc',
                        'unit': 'km'
                    }
                }
            ]
        }
        return self._execute_query(query)

    def filter_by_features(self, features: List[str], size: int = 10) -> Dict[str, Any]:
        """
        Filter restaurants by features.

        Args:
            features: List of features (e.g., ['Parking', 'Reservations', 'Wifi'])
            size: Number of results to return

        Returns:
            Filtered results
        """
        query = {
            'size': size,
            'query': {
                'bool': {
                    'must': [
                        {'terms': {'features': features}}
                    ]
                }
            }
        }
        return self._execute_query(query)

    def top_rated_restaurants(self, min_reviews: int = 50, size: int = 20) -> Dict[str, Any]:
        """
        Get top-rated restaurants with minimum review count.

        Args:
            min_reviews: Minimum number of reviews
            size: Number of results to return

        Returns:
            Top-rated restaurants
        """
        query = {
            'size': size,
            'query': {
                'bool': {
                    'filter': [
                        {'range': {'numberOfReviews': {'gte': min_reviews}}}
                    ]
                }
            },
            'sort': [
                {'rating': {'order': 'desc'}},
                {'numberOfReviews': {'order': 'desc'}}
            ]
        }
        return self._execute_query(query)

    def cuisine_aggregation(self, size: int = 20) -> Dict[str, Any]:
        """
        Get count of restaurants by cuisine type.

        Args:
            size: Number of cuisine types to return

        Returns:
            Aggregation results
        """
        query = {
            'size': 0,
            'aggs': {
                'cuisines': {
                    'terms': {
                        'field': 'cuisine',
                        'size': size
                    }
                }
            }
        }
        return self._execute_query(query)

    def rating_distribution(self) -> Dict[str, Any]:
        """
        Get distribution of restaurants by rating.

        Returns:
            Rating distribution
        """
        query = {
            'size': 0,
            'aggs': {
                'rating_distribution': {
                    'range': {
                        'field': 'rating',
                        'ranges': [
                            {'to': 3.0},
                            {'from': 3.0, 'to': 4.0},
                            {'from': 4.0, 'to': 4.5},
                            {'from': 4.5}
                        ]
                    }
                }
            }
        }
        return self._execute_query(query)

    def complex_query(
        self,
        cuisine: str,
        min_rating: float,
        latitude: float,
        longitude: float,
        distance: str = '10km',
        size: int = 20
    ) -> Dict[str, Any]:
        """
        Complex query: cuisine + rating + location.

        Args:
            cuisine: Cuisine type
            min_rating: Minimum rating
            latitude: Center latitude
            longitude: Center longitude
            distance: Search radius
            size: Number of results

        Returns:
            Filtered results
        """
        query = {
            'size': size,
            'query': {
                'bool': {
                    'must': [
                        {'term': {'cuisine': cuisine}},
                        {
                            'geo_distance': {
                                'distance': distance,
                                'location': {
                                    'lat': latitude,
                                    'lon': longitude
                                }
                            }
                        }
                    ],
                    'filter': [
                        {'range': {'rating': {'gte': min_rating}}}
                    ]
                }
            },
            'sort': [
                {'rating': {'order': 'desc'}},
                {
                    '_geo_distance': {
                        'location': {'lat': latitude, 'lon': longitude},
                        'order': 'asc',
                        'unit': 'km'
                    }
                }
            ]
        }
        return self._execute_query(query)


def main():
    """Run example queries."""
    queries = RestaurantQueries()

    examples = [
        ('Search by name', lambda q: q.search_by_name('pizza')),
        ('Filter by cuisine', lambda q: q.filter_by_cuisine('Italian', min_rating=4.0)),
        ('Full-text search', lambda q: q.search_text('biryani near me')),
        ('Top rated', lambda q: q.top_rated_restaurants(min_reviews=100)),
        ('Cuisine stats', lambda q: q.cuisine_aggregation()),
        ('Rating distribution', lambda q: q.rating_distribution()),
    ]

    for title, query_func in examples:
        try:
            print(f"\n{'='*60}")
            print(f"Query: {title}")
            print('='*60)
            result = query_func(queries)
            print(json.dumps(result, indent=2)[:500] + '...')
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
