from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """Test updating a cupcake"""
        with app.test_client() as client:
            # Create a cupcake in the database
            cupcake = Cupcake(flavor="Chocolate", size="Large",
                              rating=4.5, image="example.jpg")
            db.session.add(cupcake)
            db.session.commit()

            # Get the cupcake_id dynamically
            cupcake_id = cupcake.id

            # Make a PATCH request to update the cupcake
            response = client.patch(
                f'/api/cupcakes/{cupcake_id}', json={"flavor": "Vanilla"})
            updated_cupcake = Cupcake.query.get(cupcake_id)

            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertEqual(updated_cupcake.flavor, "Vanilla")

    def test_delete_cupcake(self):
        """Test deleting a cupcake"""
        with app.test_client() as client:
            # Create a cupcake in the database
            cupcake = Cupcake(flavor="Chocolate", size="Large",
                              rating=4.5, image="example.jpg")
            db.session.add(cupcake)
            db.session.commit()

            cupcake_id = cupcake.id

            # Make a DELETE request to delete the cupcake
            response = client.delete(f'/api/cupcakes/{cupcake_id}')
            deleted_cupcake = Cupcake.query.get(cupcake_id)

            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(deleted_cupcake)
