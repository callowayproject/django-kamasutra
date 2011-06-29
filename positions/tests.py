from django.test import TestCase
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.template import Template, Context, TemplateSyntaxError

from positions.models import Position, PositionContent
from positions import settings

class SimpleText(models.Model):
    """A Testing app"""
    firstname = models.CharField(blank=True, max_length=255)
    lastname = models.CharField(blank=True, max_length=255)
    favorite_color = models.CharField(blank=True, max_length=255)
    
    def __unicode__(self):
        return self.firstname


class SimpleCategory(models.Model):
    """Another Testing app"""
    name = models.CharField(max_length=255)


def render(src, ctx={}):
    return Template(src).render(Context(ctx))

class PositionsTestCase(TestCase):
    fixtures = ['test_data.json']
    def setUp(self):
        self.text1 = SimpleText.objects.get(pk=1)
        self.text2 = SimpleText.objects.get(pk=2)
        self.text3 = SimpleText.objects.get(pk=3)
        self.text4 = SimpleText.objects.get(pk=4)
        self.text5 = SimpleText.objects.get(pk=5)
        self.text6 = SimpleText.objects.get(pk=6)
        
        self.cat1 = SimpleCategory.objects.get(pk=1)
        self.cat2 = SimpleCategory.objects.get(pk=2)
        self.cat3 = SimpleCategory.objects.get(pk=3)

        self.samplePosition = Position.objects.create(name="sample_position", count=3)
        self.samplePosition.eligible_types.add(ContentType.objects.get_for_model(SimpleText))
        
    def testAddObject(self):
        """
        This test will ensure a position only allows objects for its 
        specified content types.
        """        
        # This will ensure adding a object to a position works for a position 
        # that allows all content types
        self.assertTrue(Position.objects.add_object(self.samplePosition, self.text1))
        
        # This will ensure that adding a object to a position is not allowed 
        # for a position that doesn't allow its content types, 
        self.assertFalse(Position.objects.add_object(self.samplePosition, self.cat1))
            
    def testAddSameObject(self):
        """
        This test will ensure that adding the same object twice will only
        work the first time.
        """        
        self.assertTrue(Position.objects.add_object(self.samplePosition, self.text1))
        self.assertFalse(Position.objects.add_object(self.samplePosition, self.text1))
            
    def testObjectOrder(self):
        """
        This test will ensure that the objects will properly adjust its order 
        correctly
        """
        Position.objects.add_object(self.samplePosition, self.text1)
        
        pc = Position.objects.get_content(self.samplePosition, as_contenttype=False)
        
        # obj1 should have the order of 1
        self.assertEqual(pc[0].order, 1)
        
        # Add a second object to the position
        Position.objects.add_object(self.samplePosition, self.text2)
        
        pc = Position.objects.get_content(self.samplePosition, as_contenttype=False)
        
        # The first object should be the object we just added obj2, and obj1 
        # should have a new order of 2
        self.assertEqual(pc[0].content_object, self.text2)
        self.assertEqual(pc[1].order, 2)
        
    def testRemove(self):
        """
        This test will ensure that removal of objects from a position will 
        properly adjust the order of the remain objects correctly, and that
        the object removed was actually removed.
        """
        Position.objects.add_object(self.samplePosition, self.text1)
        Position.objects.add_object(self.samplePosition, self.text2)
        Position.objects.add_object(self.samplePosition, self.text3)
        
        self.assertTrue(Position.objects.remove_object(self.samplePosition, self.text3))
        
        # if obj3 was added last to the position, it should have the order 
        # of 1, when we removed it the other two objects should have their
        # orders changed to 1 and 2 accordingly
        pc = Position.objects.get_content(self.samplePosition, as_contenttype=False)
        
        self.assertEqual(pc[0].content_object, self.text2)
        self.assertEqual(pc[0].order, 1)
        self.assertEqual(pc[1].content_object, self.text1)
        self.assertEqual(pc[1].order, 2)
        
    def testPrune(self):
        """
        This test will esnure that objects are pruned (removed) when the 
        position.count + CONTENT_OVERLAP_COUNT is exceeded.
        """
        Position.objects.add_object(self.samplePosition, self.text1)
        Position.objects.add_object(self.samplePosition, self.text2)
        Position.objects.add_object(self.samplePosition, self.text3)
        Position.objects.add_object(self.samplePosition, self.text4)
        Position.objects.add_object(self.samplePosition, self.text5)
        
        # Even though we specifed that this postion only hold 3 items, the
        # setting CONTENT_OVERLAP_COUNT will tell positions how many extra
        # objects to hold in the event of an object being removed.
        pc = PositionContent.objects.filter(position=self.samplePosition)
        
        # Note: Position.objects.get_content(...) will return the number of
        # items that is expected, 3 in this case. But the position will hold
        # more items, this is why we had to do a filter and not get_content
        self.assertEqual(len(pc), 5)
        
        # When we add a sixth object the position content should be pruned to
        # the position.count + CONTENT_OVERLAP_COUNT, in this case 5. And the 
        # item that should of been pruned was obj1
        Position.objects.add_object(self.samplePosition, self.text6)
        
        pc = PositionContent.objects.filter(position=self.samplePosition)
        
        self.assertEqual(len(pc), 5)
        self.assertNotEqual(pc[4], self.text1)
        
    def testGetContent(self):
        """
        This test will ensure that get_content manager method returns the 
        correct number of objects and the correct type of objects.
        """
        Position.objects.add_object(self.samplePosition, self.text1)
        Position.objects.add_object(self.samplePosition, self.text2)
        Position.objects.add_object(self.samplePosition, self.text3)
        Position.objects.add_object(self.samplePosition, self.text4)
        Position.objects.add_object(self.samplePosition, self.text5)
        
        pc1 = Position.objects.get_content(self.samplePosition)
        
        # This position should only return 3 items
        self.assertTrue(len(pc1), 3)
        
        # The default get_content returns the content objects by default.
        for item in pc1:
            self.assertTrue(isinstance(item, SimpleText))
            
        # Here we will try to retrieve more objects from the position than
        # the position specifies
        pc2 = Position.objects.get_content(self.samplePosition, count=4)
        
        self.assertTrue(len(pc2), 4)
        
        # Here will ensure the order is preserved when getting the content type
        pc3 = Position.objects.get_content(self.samplePosition, as_contenttype=False)
        pc4 = Position.objects.get_content(self.samplePosition)
        
        for count, item in enumerate(pc3):
            self.assertTrue(item.content_object, pc4[count])
        
        # Test returning the PositionContent instances enstead 
        # of the content object instance
        pc5 = Position.objects.get_content(self.samplePosition, as_contenttype=False)
        
        for item in pc5:
            self.assertTrue(isinstance(item, PositionContent))
        
    def testContainsObject(self):
        """
        This test will ensure that contains_object works correctly
        """
        Position.objects.add_object(self.samplePosition, self.text1)
        
        self.assertTrue(Position.objects.contains_object(self.samplePosition, self.text1))
        self.assertFalse(Position.objects.contains_object(self.samplePosition, self.text2))
        
    def testCanBePositioned(self):
        """
        This test will ensure that can_be_positioned works properly. This 
        function simply takes in 1 argument, the object, and checks to see 
        if any position can position it.
        """
        # Create a new position and set its only eligible type to SimpleText
        self.assertTrue(Position.objects.can_be_positioned(self.text1))
        self.assertFalse(Position.objects.can_be_positioned(self.cat1))
        
    def testIsApplicable(self):
        """
        This test will ensure that is_applicable works properly. This manager 
        method ensures that an object can be placed in a position
        """
        self.assertTrue(Position.objects.is_applicable(self.samplePosition, self.text1))
        self.assertFalse(Position.objects.is_applicable(self.samplePosition, self.cat1))
        
    def testGetApplicable(self):
        """
        get_applicable will return all the positions a specfied object can be 
        placed in. Optional argument return_all can be specified to return 
        all the positions including the positions the object is already in. 
        Default will return all positions without the current positions the 
        object is in
        """
        # First we will test a object that has not been placed in a position
        # yet, but a position does allow its content type (samplePosition)
        positions = Position.objects.get_applicable(self.text1)
        
        self.assertEqual(len(positions), 1)
        self.assertEqual(positions[0], self.samplePosition)
        
        # Next we will add text2 to samplePositions and return its applicable 
        # positions, which by default, should return none
        Position.objects.add_object(self.samplePosition, self.text2)
        positions = Position.objects.get_applicable(self.text2)
        
        self.assertEqual(len(positions), 0)
        
        # Last test will specify return_all=True, to return all the positions 
        # for text2, this should return all the positions and the positions
        # it is currently in.
        positions = Position.objects.get_applicable(self.text2, return_all=True)
        
        self.assertEqual(len(positions), 1)
        self.assertEqual(positions[0], self.samplePosition)
        
    def testTTGetPosition(self):
        """
        {% get_position [name] as [varname] %}
        {% get_position [prefix] [name] as [varname] %}
        {% get_position [name] as [varname] [slugify=True] }
        {% get_position [prefix] [name] as [varname] [slugify=True] %}
        """
        # Simple tests
        t = "{% load position_tags %}{% get_position sample_position as p %}{{ p.name }}"
        self.assertEqual(render(t), "sample_position")
        
        # If the case of a missing position, the template tag doesnt return anything
        t = "{% load position_tags %}{% get_position missing_position as p %}{{ p.name }}"
        self.assertEqual(render(t), "")
        
        # Prefix test
        pos = Position.objects.create(name="myprefix__myposition")
        t = "{% load position_tags %}{% get_position myprefix myposition as p %}{{ p.name }}"
        self.assertEqual(render(t), "myprefix__myposition")
        
        # Variable tests
        c = SimpleCategory.objects.create(name="mycategory")
        p = Position.objects.create(name="mycategory")
        
        t = "{% load position_tags %}{% get_position category.name as mycatposition %}{{ mycatposition.name }}"
        self.assertEqual(render(t, {'category': c}), "mycategory")
        
        # Variable name with variable prefix
        p = Position.objects.create(name="section__mycategory")
        t = "{% load position_tags %}{% get_position sec category.name as mycatposition %}{{ mycatposition.name }}"
        self.assertEqual(render(t, {'sec': 'section', 'category': c}), "section__mycategory")
        
        # Slugify test
        c = SimpleCategory.objects.create(name="Awesome Category")
        p = Position.objects.create(name="awesome-category")
        t = "{% load position_tags %}{% get_position category.name as mycatposition slugify=True %}{{ mycatposition.name }}"
        render(t, {'category': c})
        self.assertEqual(render(t, {'category': c}), "awesome-category")
        
    def testTTGetPositionContent(self):
        """
        {% get_position_content position as content %}
        {% get_position_content position as content [limit=N] [as_contenttype=True|False] %}
        """
        Position.objects.add_object(self.samplePosition, self.text1)
        Position.objects.add_object(self.samplePosition, self.text2)
        Position.objects.add_object(self.samplePosition, self.text3)
        
        t = "{% load position_tags %}{% get_position_content position as content %}{% for c in content %}{{ c }},{% endfor %}"
        self.assertEqual(render(t, {'position': self.samplePosition}), "Jenny,Bobby,Joe,")
        
        # Limit test
        t = "{% load position_tags %}{% get_position_content position as content limit=2 %}{% for c in content %}{{ c }},{% endfor %}"
        self.assertEqual(render(t, {'position': self.samplePosition}), "Jenny,Bobby,")
        
        # ContentType test
        t = "{% load position_tags %}{% get_position_content position as content as_contenttype=False %}{% for c in content %}{{ c.content_object }},{% endfor %}"
        self.assertEqual(render(t, {'position': self.samplePosition}), "Jenny,Bobby,Joe,")
        
    def testTTGetContentPositions(self):
        """
        {% get_content_positions object as positions %}
        {% get_content_positions content_type_id object_id as positions %}
        """
        # First test should return nothing since text1 was not adde to 
        # samplePosition yet
        t = "{% load position_tags %}{% get_content_positions obj as positions %}{% for p in positions %}{{ p.name }}{% endfor %}"
        self.assertEqual(render(t, {'obj': self.text1}), "")
        
        Position.objects.add_object(self.samplePosition, self.text1)
        
        t = "{% load position_tags %}{% get_content_positions obj as positions %}{% for p in positions %}{{ p.name }}{% endfor %}"
        self.assertEqual(render(t, {'obj': self.text1}), "sample_position")
        
        # content_type_id and object_id test
        ctype = ContentType.objects.get_for_model(self.text1)
        t = "{% load position_tags %}{% get_content_positions ctype.pk object.pk as positions %}{% for p in positions %}{{ p.name }}{% endfor %}"
        self.assertEqual(render(t, {"ctype": ctype, "object": self.text1}), "sample_position")
        
    def testTTGetApplicable(self):
        """
        {% get_applicable_positions object as positions [all] %}    
        {% get_applicable_positions content_type_id object_id as positions [all] %}
        """
        t = "{% load position_tags %}{% get_applicable_positions obj as positions %}{% for p in positions %}{{ p.name }}{% endfor %}"
        self.assertEqual(render(t, {'obj': self.text1}), "sample_position")
        
        # content_type_id and object_id test
        ctype = ContentType.objects.get_for_model(self.text1)
        t = "{% load position_tags %}{% get_applicable_positions ctype.pk object.pk as positions %}{% for p in positions %}{{ p.name }}{% endfor %}"
        self.assertEqual(render(t, {"ctype": ctype, "object": self.text1}), "sample_position")
        
        # All test: When we add text1 to samplePosition, nothing should be returned
        Position.objects.add_object(self.samplePosition, self.text1)
        t = "{% load position_tags %}{% get_applicable_positions obj as positions %}{% for p in positions %}{{ p.name }}{% endfor %}"
        self.assertEqual(render(t, {'obj': self.text1}), "")
        
        # With "all" specified, even the positions text1 has been added to should be returned
        t = "{% load position_tags %}{% get_applicable_positions obj as positions all %}{% for p in positions %}{{ p.name }}{% endfor %}"
        self.assertEqual(render(t, {'obj': self.text1}), "sample_position")
        
    def testTTCanBePositioned(self):
        """
        {% can_be_positioned [object] as [varname] %}
        {% can_be_positioned [content_type_id] [object_id] as [varname] %}
        """
        t = "{% load position_tags %}{% can_be_positioned object as canbe %}{% if canbe %}TRUE{% else %}FALSE{% endif %}"
        self.assertEqual(render(t, {"object": self.text1}), "TRUE")
        
        t = "{% load position_tags %}{% can_be_positioned object as canbe %}{% if canbe %}TRUE{% else %}FALSE{% endif %}"
        self.assertEqual(render(t, {"object": self.cat1}), "FALSE")
        
        # content_type_id and object_id test
        ctype = ContentType.objects.get_for_model(self.text1)
        t = "{% load position_tags %}{% can_be_positioned ctype.pk object.pk as canbe %}{% if canbe %}TRUE{% else %}FALSE{% endif %}"
        self.assertEqual(render(t, {"object": self.text1, "ctype": ctype}), "TRUE")
        
    def testTTRenderPositionContent(self):
        """
        {% render_position_content [PositionContent] [with] [suffix=S] [template=T] %}
        {% render_position_content pc %}
        """
        Position.objects.add_object(self.samplePosition, self.text1)
        
        pc = Position.objects.get_content(self.samplePosition, as_contenttype=False)[0]
        
        t = "{% load position_tags %}{% render_position_content pc %}"
        self.assertEqual(render(t, {"pc": pc}), "<div>1 - Joe</div>")
        
        t = "{% load position_tags %}{% render_position_content pc with template=position_test/custom_template.html %}"
        self.assertEqual(render(t, {"pc": pc}), "<div>CUSTOM - 1 - Joe</div>")
        