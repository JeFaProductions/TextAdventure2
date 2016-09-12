import unittest
import tead.event as evt

class TestEventSystem(unittest.TestCase):

    def myCallback(self, event):
        self.called = self.called + 1

        self.assertEqual('test', event.type)
        self.assertIn('foo', event.userParam)
        self.assertEqual('bar', event.userParam['foo'])

    def setUp(self):
        self.system = evt.EventSystem()
        self.called = 0

    def testRegisterEventHandler(self):
        self.assertNotIn('test', self.system._eventHandlers)

        self.system.registerEventHander('test', self.myCallback)

        self.assertIn('test', self.system._eventHandlers, 'no list created')
        self.assertEqual(1, len(self.system._eventHandlers['test']), 'no handler added')

    def testUnregisterEventHandler(self):
        self.assertNotIn('test', self.system._eventHandlers)

        handlerID = self.system.registerEventHander('test', self.myCallback)

        self.assertIn('test', self.system._eventHandlers)
        self.assertEqual(1, len(self.system._eventHandlers['test']))

        self.system.unregisterEventHandler('test', handlerID)

        self.assertIn('test', self.system._eventHandlers, 'list was deleted')
        self.assertEqual(0, len(self.system._eventHandlers['test']), 'handler was not removed')

    def testCreateEvent(self):
        self.assertEqual(0, self.system._eventQueue.qsize())

        self.system.createEvent(evt.Event(eventType='test', userParam={'foo' : 'bar'}))

        self.assertEqual(1, self.system._eventQueue.qsize(), 'queue has still no event')

    def testProcessEvent(self):
        self.system.registerEventHander('test', self.myCallback)
        self.system.createEvent(evt.Event(eventType='test', userParam={'foo' : 'bar'}))
        self.system.createEvent(evt.Event(eventType='test', userParam={'foo' : 'bar'}))

        self.assertFalse(self.system._eventQueue.empty())
        self.assertEqual(0, self.called)

        self.system.processEvents()

        self.assertTrue(self.system._eventQueue.empty())
        self.assertEqual(2, self.called)

