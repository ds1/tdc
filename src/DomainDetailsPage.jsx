import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { MessageSquare, DollarSign, Globe, Calendar } from 'lucide-react';

const DomainDetailsPage = ({ domain }) => {
  // For demo, using the first domain from the data
  const defaultDomain = {
    domainName: "18.bot",
    price: 1000000,
    category: "bot",
    tld: "bot",
    imageUrl: "/data/output/thumbnails/18_bot.jpg",
    length: 2
  };

  const activeDomain = domain || defaultDomain;
  const [message, setMessage] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission here
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      {/* Hero Section */}
      <div className="bg-white shadow-sm mb-8">
        <div className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                {activeDomain.domainName}
              </h1>
              <div className="flex items-center mb-6">
                <DollarSign className="h-6 w-6 text-green-600 mr-2" />
                <span className="text-3xl font-bold text-green-600">
                  ${activeDomain.price.toLocaleString()}
                </span>
              </div>
              <div className="space-y-4">
                <div className="flex items-center text-gray-600">
                  <Calendar className="h-5 w-5 mr-2" />
                  <span>Listed: October 2024</span>
                </div>
              </div>
            </div>
            <div className="rounded-lg overflow-hidden shadow-lg">
              <img
                src={activeDomain.imageUrl}
                alt={activeDomain.domainName}
                className="w-full h-64 object-cover"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.parentElement.innerHTML = `
                    <div class="w-full h-64 bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
                      <span class="text-white text-3xl font-bold">${activeDomain.domainName}</span>
                    </div>
                  `;
                }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Domain Description */}
          <div className="md:col-span-2">
            <Card className="p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">About This Domain</h2>
              <div className="prose max-w-none">
                <p className="text-gray-600 mb-4">
                  {activeDomain.domainName} is a premium {activeDomain.length}-character domain name 
                  in the {activeDomain.category} category with a .{activeDomain.tld} extension. 
                  This memorable domain is perfect for:
                </p>
                <ul className="list-disc pl-5 space-y-2 text-gray-600">
                  <li>Building a strong brand in the {activeDomain.category} industry</li>
                  <li>Launching a new product or service</li>
                  <li>Creating a memorable online presence</li>
                  <li>Protecting your brand identity</li>
                </ul>
              </div>
            </Card>
          </div>

          {/* Contact Form */}
          <div className="md:col-span-1">
            <Card className="p-6">
              <div className="flex items-center mb-4">
                <MessageSquare className="h-5 w-5 text-blue-600 mr-2" />
                <h2 className="text-xl font-bold text-gray-900">Inquire About This Domain</h2>
              </div>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="email">Your Email</Label>
                  <Input 
                    type="email" 
                    id="email" 
                    placeholder="you@example.com" 
                    required 
                  />
                </div>
                <div>
                  <Label htmlFor="subject">Subject</Label>
                  <Input 
                    type="text" 
                    id="subject" 
                    value={`Inquiry about ${activeDomain.domainName}`} 
                    readOnly 
                  />
                </div>
                <div>
                  <Label htmlFor="message">Message</Label>
                  <Textarea 
                    id="message" 
                    placeholder="I'm interested in purchasing this domain..." 
                    required
                    className="h-32"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                  />
                </div>
                <Button type="submit" className="w-full">
                  Send Inquiry
                </Button>
              </form>
              
              {submitted && (
                <Alert className="mt-4">
                  <AlertDescription>
                    Thank you for your inquiry. We'll get back to you shortly.
                  </AlertDescription>
                </Alert>
              )}
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DomainDetailsPage;