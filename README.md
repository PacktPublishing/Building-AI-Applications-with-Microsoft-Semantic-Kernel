# Building AI Applications with Microsoft Semantic Kernel

<a href="https://www.packtpub.com/product/building-ai-agents-with-microsoft-semantic-kernel/9781835463703"><img src="https://content.packt.com/B21826/cover_image_small.jpg" alt="" height="256px" align="right"></a>

This is the code repository for [Building AI Applications with Microsoft Semantic Kernel](https://www.packtpub.com/product/building-ai-agents-with-microsoft-semantic-kernel/9781835463703), published by Packt.

**Easily integrate generative AI capabilities and copilot experiences into your applications**

## What is this book about?
In the fast-paced world of AI, developers are constantly seeking efficient ways to integrate AI capabilities into their apps. Microsoft Semantic Kernel simplifies this process by using the GenAI features from Microsoft and OpenAI.
	
This book covers the following exciting features:
* Write reusable AI prompts and connect to different AI providers
* Create new plugins that extend the capabilities of AI services
* Understand how to combine multiple plugins to execute complex actions
* Orchestrate multiple AI services to accomplish a task
* Leverage the powerful planner to automatically create appropriate AI calls
* Use vector databases as additional memory for your AI tasks
* Deploy your application to ChatGPT, making it available to hundreds of millions of users

If you feel this book is for you, get your [copy](https://www.amazon.com/dp/1835463703) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" 
alt="https://www.packtpub.com/" border="5" /></a>


## Instructions and Navigations
All of the code is organized into folders. For example, ch2.

The code will look like the following:
```
    response = await kernel.invoke(pe_plugin["chain_of_thought"],
KernelArguments(problem = problem, input = solve_steps))
    print(f"\n\nFinal answer: {str(response)}\n\n")
```

**Following is what you need for this book:**

This book is for beginner-level to experienced .NET or Python software developers who want to quickly incorporate the latest AI technologies into their applications, without having to learn the details of every new AI service. Product managers with some development experience will find this book helpful while creating proof-of-concept applications. This book requires working knowledge of programming basics.

With the following software and hardware list you can run all code files present in the book (Chapter 1-8).

## Software and Hardware List

| Chapter  | Software required           | OS required                      |
| -------- | ----------------------------| ---------------------------------|
| 1-8      | Python 3.11                 | Windows, macOS, or Linux         |
| 1-8      | .NET 8                      | Windows, macOS, or Linux         |
| 1-8      | OpenAI GPT-3.5 and GPT-4    | Windows, macOS, or Linux         |


## Related products <Other books you may enjoy>
* OpenAI API Cookbook [[Packt]](https://www.packtpub.com/product/openai-api-cookbook/9781805121350) [[Amazon]](https://www.amazon.com/dp/1805121359)

* Modern Data Architecture on AWS [[Packt]](https://www.packtpub.com/product/modern-data-architecture-on-aws/9781801813396) [[Amazon]](https://www.amazon.com/dp/1801813396)

## Errata
* Page 33, Last code snippet
  ```
  dotnet add package Microsoft.SemanticKernel.
  s.Handlebars --version 1.0.1-preview
  ```
  _should be_
  ```
  dotnet add package Microsoft.SemanticKernel.planners.Handlebars --version 1.0.1-preview
  ```

## Get to Know the Author
**Lucas A. Meyer**
is a Computer Scientist and Financial Economist with over two decades of experience in technology. Lucas joined Microsoft in 2002 to work with databases in Finance, joined Amazon in 2020 to work with detection and prevention, and returned to Microsoft in 2022 as a Principal Research Scientist in the Microsoft&rsquo;s AI for Good Lab, where he works with Large Language Models (LLMs) and the Microsoft Semantic Kernel daily.
Lucas&rsquo; first NLP project, released in 2016, was a chatbot that streamlined several corporate finance operations and won the Adam Smith Award from London&rsquo;s Treasury Today. Lucas has an MBA and an M.Sc. in Finance from the University of Washington in Seattle.
